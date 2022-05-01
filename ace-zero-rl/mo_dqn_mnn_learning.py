#!/usr/bin/env python3
import sys
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.activity.learning import Learning
from rl2020.listener.impl.redefined_reward_console_log_listener import RedefinedRewardConsoleLogListener
from rl2020.morl.morl_file_log_listener import MultiObjectiveFileLogListener
from rl2020.agent_builder.agent_builder import AgentBuilder
from rl2020.agent.mo_mnn_dqn_agent import MultiObjectiveMultiNNDQNAgent
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_011 import AceZeroMORLRewardBuilder011
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_012 import AceZeroMORLRewardBuilder012
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_013 import AceZeroMORLRewardBuilder013
from rl2020.env.acezero.listener.acezero_random_position_initializer_in_square import AceZeroRandomPositionInitializerInSquare
from rl2020.morl.morl_policy_maker import MultiObjectivePolicyMaker
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_001 import AceZeroMORLRewardBuilder001
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_002 import AceZeroMORLRewardBuilder002
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_003 import AceZeroMORLRewardBuilder003

class AceZeroDQNMOAgentBuilder(AgentBuilder):
    def create_agent(self, seed, initial_policy_path=None):
        memory_size = 1_000_000; batch_size = 64; dqn_dims = [4, 300, self.num_actions]
        return MultiObjectiveMultiNNDQNAgent(memory_size, batch_size, dqn_dims, self.normalizer, reward_builder, seed)
    
if __name__ == '__main__':
    scenario_name = 'dummy.json' #'basic-001.json'
    results_name = 'dqn-mo-mnn-random-20000-rb002'
    out_path = 'rl2021_mo_results/dqn-mo-mnn/' + results_name
    start_trial = 2; num_trials = 3; num_episodes = 20_000
#     reward_builder = AceZeroMORLRewardBuilder001()
    reward_builder = AceZeroMORLRewardBuilder002()
    num_rewards = reward_builder.get_num_rewards()
    max_steps_per_episode = 700;
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZeroEnvironment(scenario_name)    
    learning = Learning()
    learning.add_listener(RedefinedRewardConsoleLogListener())
    learning.add_listener(MultiObjectiveFileLogListener());
    learning.add_listener(MultiObjectivePolicyMaker(1, 0.1, num_rewards));
    #learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    agent_builder = AceZeroDQNMOAgentBuilder(len(env.actions), normalizer=AceZeroDQNNormalizer())
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)