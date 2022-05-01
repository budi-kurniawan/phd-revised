#!/usr/bin/env python3
import sys
from rl2020.agent.dqn_agent import DQNAgent
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.activity.learning import Learning
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
from rl2020.agent_builder.agent_builder import AgentBuilder
from rl2020.env.acezero.env_reward_builder.acezero_env_reward_builder_001 import AceZeroEnvironmentRewardBuilder001
from rl2020.listener.impl.basic_functions import BasicFunctions
from rl2020.agent.dqn_wtn_agent import DQNWithTargetNetworkAgent
from rl2020.agent.double_dqn_agent import DoubleDQNAgent
from rl2020.agent.double_dqn_agent2 import DoubleDQNAgent2
from rl2020.env.acezero.listener.acezero_random_position_initializer_in_square import AceZeroRandomPositionInitializerInSquare
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.file_log_listener import FileLogListener
from rl2020.listener.impl.policy_maker import PolicyMaker

class AceZeroDQNAgentBuilder(AgentBuilder):
    def create_agent(self, seed, initial_policy_path=None):
        memory_size = 1_000_000; batch_size = 64; dqn_dims = [4, 300, self.num_actions]
        target_refresh_interval = 700 # for DQNWithTargetNetwork
        return DQNAgent(memory_size, batch_size, dqn_dims, self.normalizer, seed)
        #return DQNWithTargetNetworkAgent(memory_size, batch_size, dqn_dims, self.normalizer, target_refresh_interval, seed)
        #return DoubleDQNAgent(memory_size, batch_size, dqn_dims, self.normalizer, seed)
        #return DoubleDQNAgent2(memory_size, batch_size, dqn_dims, self.normalizer, seed)
    
if __name__ == '__main__':
    scenario_name = 'basic-005.json'
    #results_name = 'dqn-wtn-c700-005'
    results_name = 'dqn-random'
#     out_path = 'rl2020_results/dqn-so/' + results_name
    #results_name = 'dqn-wtn-c700-random'
    out_path = 'rl2020_results/dqn-so/' + results_name
#     results_name = 'double-dqn-random' #'double-dqn-005'
#    out_path = 'rl2020_results/double-dqn-so/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 20_000
    max_steps_per_episode = 700; chart_offset = 0.5
    env_reward_builder = None #AceZeroEnvironmentRewardBuilder001()
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZeroEnvironment(scenario_name, env_reward_builder)    
    learning = Learning()
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    milestone_episodes = [10_000]
    learning.add_listener(PolicyMaker(2, 0.1, milestone_episodes));
    #learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    agent_builder = AceZeroDQNAgentBuilder(len(env.actions), normalizer=AceZeroDQNNormalizer(), agent_load_path=out_path)
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)