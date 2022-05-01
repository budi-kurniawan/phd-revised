import sys
import os
import random
#import pickle
import time
import math
import numpy as np
from random import seed
from random import random

from pathlib import Path
from ace_zero_core.acezero import ACEZero
from ace_zero_core import *
from ace_zero_core.utils import constrain_180
import rl.rl_utils
from rl import *
from rl.context import Context
from rl.agent.controllable import ControllableAgent
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment

class AceZeroRLVsRLEnvironment(AceZeroEnvironment):
    actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']
    
    def __init__(self, scenario_name, cobra_tester):
        super().__init__(scenario_name)
        self.cobra_tester = cobra_tester
        self.cobra_state = None

    """ reset() creates a new instance of viper and cobra. """
    def reset(self):
        self.ace0 = ACEZero(scenario_uri=self.base_scenario_path, root_path=self.ace_zero_core_path, 
                out_path=self.results_path, data_path=self.data_path)
        #self.ace0 = acezero.ACEZero(scenario_uri=self.base_scenario_path, root_path=self.ace_zero_core_path, 
        #        out_path=self.out_path, data_path=self.data_path)
        ace0 = self.ace0
        context = Context(self.root_path, self.scenario_path)
        rl_utils.context = context
        context.blue_initial = {**rl_utils.blue_default_initial}
        context.red_initial = {**rl_utils.red_default_initial}
        self.do_config_fighter(ace0.sim, self.scenario_path, context)
        self.sim = ace0.sim
        sim = self.sim
        viper, cobra = sim.viper, sim.cobra
        viper.contact_assessment(viper.get_state(), cobra.get_state())
        self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v)
        cobra.contact_assessment(cobra.get_state(), viper.get_state())
        self.cobra_state = (cobra.contact_range, cobra.contact_aa, cobra.contact_ata, cobra.delta_v)
        #print('viper_state after reset:', self.state, ', cobra_state_aft reset:', self.cobra_state)
        return np.array(self.state)

    def step(self, action):
        sim = self.sim
        sim.current_time = round(sim.current_time, 1)
        sim.dt = round(sim.dt, 1)
        viper, cobra = sim.viper, sim.cobra
        
#         if sim.current_time < 2:
#             print(sim.current_time, 'viper:', viper.fcs.platform.x, viper.fcs.platform.y, viper.fcs.platform.z, viper.fcs.platform.psi)
#             print('cobra:', cobra.fcs.platform.x, cobra.fcs.platform.y, cobra.fcs.platform.z, cobra.fcs.platform.psi)
        
        if isinstance(viper.pilot, ControllableAgent):
            viper.pilot.set_action(self.actions[action])
        if isinstance(cobra.pilot, ControllableAgent):
            cobra_action = self.cobra_tester.select_action(np.array(self.cobra_state))
            cobra.pilot.set_action(self.actions[cobra_action])
#             if sim.current_time == 0:
#                 print('action:', action, ', cobra action:', cobra_action)
        sim.tick(sim.current_time, sim.dt)
        self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v)
        self.cobra_state = (cobra.contact_range, cobra.contact_aa, cobra.contact_ata, cobra.delta_v)
        #print('viper state:', self.state, ', cobra_state:', self.cobra_state)
        sim.current_time += sim.dt
        data = {'entity_state' : viper.pilot.beliefs.entity_state, 'threat_state' : viper.pilot.beliefs.threat_state, 
                'viper':viper, 'cobra':cobra, 'current_time':sim.current_time, 'dt':sim.dt, 'cobra_state':self.cobra_state,
                'cobra_action':cobra_action}
        reward = viper.mcgrew_score - 0.5
        done = False
        return np.array(self.state), reward, done, data