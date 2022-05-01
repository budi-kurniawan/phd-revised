#!/usr/bin/env python3
import sys
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.listener.impl.policy_maker import PolicyMaker
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.activity.learning import Learning
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000
from rl2020.listener.impl.redefined_reward_console_log_listener import RedefinedRewardConsoleLogListener
from rl2020.morl.morl_file_log_listener import MultiObjectiveFileLogListener
from rl2020.agent_builder.impl.mo_q_learning_traces_agent_builder import MultiObjectiveQLearningTracesAgentBuilder
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_008 import AceZeroMORLRewardBuilder008
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_001 import AceZeroMORLRewardBuilder001
from rl2020.morl.morl_policy_maker import MultiObjectivePolicyMaker
from rl2020.env.acezero.listener.acezero_random_position_initializer_in_square import AceZeroRandomPositionInitializerInSquare
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_002 import AceZeroMORLRewardBuilder002
from rl2020.env.acezero.reward_builder.acezero_morl_reward_builder_003 import AceZeroMORLRewardBuilder003

if __name__ == '__main__':
    scenario_name = 'dummy.json'
    results_name = 'ql-mo-random-200000-rb003'
    out_path = 'rl2021_mo_results/ql-mo/' + results_name
    reward_builder = AceZeroMORLRewardBuilder003()
    env_reward_builder = None #AceZeroEnvironmentRewardBuilder101()
    start_trial = 0; num_trials = 1; num_episodes = 200_000
    max_steps_per_episode = 700;
    chart_offset = 0.5
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZeroEnvironment(scenario_name, env_reward_builder)

    learning = Learning()
    learning.add_listener(RedefinedRewardConsoleLogListener())
    learning.add_listener(MultiObjectiveFileLogListener());
    learning.add_listener(MultiObjectivePolicyMaker(1, 0.2, reward_builder.get_num_rewards()));
    #learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    agent_builder = MultiObjectiveQLearningTracesAgentBuilder(len(env.actions), discretizer=AceZeroDiscretizer14000(), 
            reward_builder=reward_builder)
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)