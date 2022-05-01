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

class AceZero3DEnvironment(AceZeroEnvironment):
    actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'speed_pct(-10)', 'speed_pct(10)', 'altitude(-10)', 'altitude(10)']

    """ reset() creates a new instance of viper and cobra. """
    def reset(self):
        super().reset()
        sim = self.sim
        viper, cobra = sim.viper, sim.cobra
        delta_z = viper.get_state().z - cobra.get_state().z
        self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v, delta_z)
        return np.array(self.state)

    def step(self, action):
        sim = self.sim
        sim.current_time = round(sim.current_time, 1)
        sim.dt = round(sim.dt, 1)
        viper, cobra = sim.viper, sim.cobra
        if isinstance(viper.pilot, ControllableAgent):
            viper.pilot.set_action(self.actions[action])
        
        sim.tick(sim.current_time, sim.dt)
        delta_z = viper.get_state().z - cobra.get_state().z
        self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v, delta_z)
        reward = viper.mcgrew_score - 0.5
        done = False
        sim.current_time += sim.dt
        data = {'entity_state' : viper.pilot.beliefs.entity_state, 'threat_state' : viper.pilot.beliefs.threat_state}
        return np.array(self.state), reward, done, data