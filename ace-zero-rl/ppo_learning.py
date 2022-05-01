#!/usr/bin/env python3
"""
    Cartpole learning with PPO
"""
import sys
from rl2020.env.acezero.listener.acezero_random_position_initializer_in_square import AceZeroRandomPositionInitializerInSquare
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
from rl2020.activity.learning import Learning
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.file_log_listener import FileLogListener
from rl2020.listener.impl.policy_maker import PolicyMaker
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
sys.path.insert(0, "../spyrl")
from spyrl.agent_builder.agent_builder import AgentBuilder
from spyrl.agent.impl.ppo_agent import PPOAgent
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment

__author__ = "Budi Kurniawan"
__copyright__ = "Copyright 2021, Budi Kurniawan"
__license__ = "GPL"
__version__ = "0.1.0"

class PPOAgentBuilder(AgentBuilder):
    def create_agent(self, seed, initial_policy_path=None):
        return PPOAgent(nn_dims, self.normaliser, seed)
        #return PPOAgent(nn_dims, self.normaliser, seed, local_steps_per_epoch=700, max_ep_len=175)
        #return PPOAgent(nn_dims, self.normaliser, seed, local_steps_per_epoch=100, max_ep_len=25)

if __name__ == '__main__':
    scenario_name = 'dummy.json' #'basic-004.json'
    results_name = 'ppo4K-random'
    out_path = 'rl2020_results/ppo-so/' + results_name
    max_steps_per_episode = 700; chart_offset = 0.5
    env_reward_builder = None #AceZeroEnvironmentRewardBuilder001()
    start_trial = 0
    num_trials = 1
    num_episodes = 20_000
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZeroEnvironment(scenario_name, env_reward_builder)    
    learning = Learning()
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    milestone_episodes = [10_000]
    learning.add_listener(PolicyMaker(1, 0.1, milestone_episodes));

    num_actions = 5
    num_state_vars = 4
    nn_dims = (num_state_vars, 300, 300, num_actions)
    
    #learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    agent_builder = PPOAgentBuilder(nn_dims, normaliser=AceZeroDQNNormalizer(), agent_load_path=out_path)    
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)
