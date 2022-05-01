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

class ActionSpace(object):
    pass

class AceZeroEnvironment():
    actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']
    #actions = ['set_heading(10)', 'set_heading(-10)']
    
    def __init__(self, scenario_name, reward_builder=None):
        self.scenario_name = scenario_name
        self.root_path = Path(os.getcwd())
        self.ace_zero_core_path = self.root_path / Path("ace_zero_core")
        self.data_path = self.root_path / Path("rl_data")
        self.base_scenario_path = self.data_path / Path("scenarios/base.json")        
        self.scenario_path = self.data_path / Path("scenarios/" + self.scenario_name)
        self.results_path = self.root_path / Path("rl_results")
        self.reward_builder = reward_builder
        """ disable action_space because it won't change dynamically if we override actions """
        #self.action_space = ActionSpace() # added compatibility with openai Gym
        #self.action_space.n = len(AceZeroEnvironment.actions)

    def change_scenario(self, scenario_name):
        self.scenario_name = scenario_name
        self.scenario_path = self.data_path / Path("scenarios/" + self.scenario_name)
        self.reset() # essentially create a new instance of ACEZero

    """ reset() creates a new instance of viper and cobra. """
    def reset(self):
        #self.ace0 = ACEZero(scenario_uri=self.base_scenario_path, root_path=self.ace_zero_core_path, out_path=self.results_path, data_path=self.data_path)
        self.ace0 = ACEZero(self.base_scenario_path, self.ace_zero_core_path, self.results_path, self.data_path)
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
        if self.reward_builder is not None:
            self.reward_builder.reset()
        return np.array(self.state)

    def step(self, action):
        sim = self.sim
        sim.current_time = round(sim.current_time, 1)
        sim.dt = round(sim.dt, 1)
        viper = sim.viper
        if isinstance(viper.pilot, ControllableAgent):
            viper.pilot.set_action(self.actions[action])
        sim.tick(sim.current_time, sim.dt)
        self.state = (viper.contact_range, viper.contact_aa, viper.contact_ata, viper.delta_v)
        sim.current_time += sim.dt
        data = {'entity_state' : viper.pilot.beliefs.entity_state, 'threat_state' : viper.pilot.beliefs.threat_state, 
                'viper':viper, 'cobra':sim.cobra, 'current_time':sim.current_time, 'dt':sim.dt}
        if self.reward_builder is None:
            reward = viper.mcgrew_score - 0.5
            done = False
        else:
            reward = self.reward_builder.get_reward(data)
            done = self.reward_builder.is_terminal()
        return np.array(self.state), reward, done, data
    
    def show_trajectory_chart(self):
        self.ace0.show_trajectory_chart()
    
    def seed(self, seed):
        pass # do nothing for now

    def do_config_fighter(self, sim, config_file, context): # copied from rl_Utils.config_fighter and modified
        import json
        if not hasattr(context, 'config'):
            if not os.path.exists(config_file):
                raise SystemExit("Script action file '{}' does not exist".
                    format(config_file))
            try:
                with open(config_file) as instream:
                    context.config = json.load(instream)
            except IOError as e:
                raise SystemExit("Error opening scenario file '{}'\n{}".
                    format(config_file, str(e)))
            
        config = context.config
        if 'dt' in config:
            sim.dt = config['dt']
            print('user-defined dt:', sim.dt)
        if 'max_ticks' in config:
            sim.umpire.termination_triggers[0].max_time_elapsed = sim.dt * config['max_ticks']
    
        if 'blue' in config:
            blue = config['blue']
            if 'dyn_initials' in blue:
                for dyn_initial in blue['dyn_initials']:
                    if context.episode == dyn_initial['episode']:
                        context.blue_initial.update(dyn_initial['initial'])
    
            initial = {**context.blue_initial}
            if 'initial' in blue:
                initial.update(blue['initial'])
            agent_params = blue['agent_params'] if 'agent_params' in blue else {}
            sim.viper = sim.get_fighter(initial, blue['agent_class'], agent_params)
            
        if 'red' in config:
            red = config['red']
            initial = {**context.red_initial}
            if 'initial' in red:
                initial.update(red['initial'])
            agent_params = red['agent_params'] if 'agent_params' in red else {}
            sim.cobra = sim.get_fighter(initial, red['agent_class'], agent_params)
