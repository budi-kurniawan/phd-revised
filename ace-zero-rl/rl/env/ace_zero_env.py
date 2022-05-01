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
from ace_zero_core import *
from ace_zero_core.utils import constrain_180
from rl import *
from rl.context import Context

class ActionSpace(object):
    pass

class AceZeroEnvironment():
    actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']
    #actions = ['set_heading(10)', 'set_heading(-10)']
    
    def __init__(self, scenario_name):
        self.scenario_name = scenario_name
        self.root_path = Path(os.getcwd())
        self.ace_zero_core_path = self.root_path / Path("ace_zero_core")
        self.data_path = self.root_path / Path("rl_data")
        self.base_scenario_path = self.data_path / Path("scenarios/base.json")
        self.scenario_path = self.data_path / Path("scenarios/" + self.scenario_name)
        self.results_path = self.root_path / Path("rl_results")
        self.action_space = ActionSpace() # added compatibility with openai Gym
        self.action_space.n = len(AceZeroEnvironment.actions)

    """ reset() creates a new instance of viper and cobra. """
    def reset(self, blue_initials=None, red_initials=None):
        self.ace0 = acezero.ACEZero(scenario_uri=self.base_scenario_path, root_path=self.ace_zero_core_path, 
                out_path=self.results_path, data_path=self.data_path)
        ace0 = self.ace0
        context = Context(self.root_path, self.scenario_path)
        rl_utils.context = context
        context.blue_initial = {**rl_utils.blue_default_initial}
        context.red_initial = {**rl_utils.red_default_initial}
        if red_initials is not None:
            context.red_initial['x'] = red_initials[0]
            context.red_initial['y'] = red_initials[1]
            context.red_initial['z'] = red_initials[2]
            context.red_initial['psi'] = red_initials[3]
        #print('context.red_initial after:', context.red_initial)
        rl_utils.config_fighter(ace0.sim, self.scenario_path, context)
        self.sim = ace0.sim
        sim = self.sim
        viper, cobra = sim.viper, sim.cobra
        viper.contact_assessment(viper.get_state(), cobra.get_state())
        #delta_psi = viper.get_state().psi - cobra.get_state().psi
        #delta_psi = constrain_180(delta_psi)
        #self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v, delta_psi)
        self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v)
        #self.np_random, seed = seeding.np_random(seed)
        #self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        return np.array(self.state)

    def step(self, action):
        sim = self.sim
        sim.current_time = round(sim.current_time, 1)
        sim.dt = round(sim.dt, 1)
        viper = sim.viper
        viper.pilot.set_action(self.actions[action])
        sim.tick(sim.current_time, sim.dt)
        #es = viper.pilot.beliefs.entity_state
        #ts = viper.pilot.beliefs.threat_state
        #delta_psi = es.psi - ts.psi
        #delta_psi = constrain_180(delta_psi)
        #self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v, delta_psi)
        self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v)
        reward = viper.mcgrew_score - 0.5
        done = False
        sim.current_time += sim.dt
        data = {'entity_state' : viper.pilot.beliefs.entity_state, 'threat_state' : viper.pilot.beliefs.threat_state}
        return np.array(self.state), reward, done, data
    
    def show_trajectory_chart(self):
        self.ace0.show_trajectory_chart()
    
    def seed(self, seed):
        pass # do nothing for now
