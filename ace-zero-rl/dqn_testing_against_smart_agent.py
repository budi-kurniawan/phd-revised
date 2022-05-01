#!/usr/bin/env python3
import sys
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.listener.acezero_trajectory_manager import AceZeroTrajectoryManager
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.activity.testing import Testing
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.env.acezero.listener.acezero_basic_test_b import AceZeroBasicTestB
from rl2020.env.acezero.listener.acezero_basic_test_c import AceZeroBasicTestC
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
from rl2020.tester_builder.impl.dqn_tester_builder import DQNTesterBuilder
from rl2020.tester_builder.impl.mo_dqn_tester_builder import MultiObjectiveDQNTesterBuilder
from rl2020.tester_builder.impl.mo_mnn_dqn_tester_builder import MultiObjectiveMultiNNDQNTesterBuilder
from rl2020.env.acezero.listener.acezero_blue_red_result_logger import AceZeroBlueRedResultLogger

if __name__ == '__main__':
    
    """ 
    1. Change the agent_type
    2. Change num_learning_episodes
    3. change d2dsql_policy
    """
    
    agent_type = 'pure-pursuit'
    agent_type = 'smart-pursuit'
    agent_type = 'stern-conversion'
    #agent_type = 'restricted-pure-pursuit'
    #agent_type = 'restricted-smart-pursuit'
    #agent_type = 'restricted-stern-conversion'
    
    d2dsql_policy = 'dqn-002' #'dqn-random'
    
    if len(sys.argv) > 1:
        agent_type = sys.argv[1]

    num_learning_episodes = 20000
    description = d2dsql_policy + '-' + str(num_learning_episodes) + ' vs red_' + agent_type + ' (Basic A)'
    scenario_name = 'red-' + agent_type + '-agent.json'

    results_name = d2dsql_policy + '-' + str(num_learning_episodes) + '-red-' + agent_type + '-basic-a'    
    out_path = 'rl2020_test_results/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 200; num_steps = 700
    
    policy_parent_path = 'rl2020_results/' + d2dsql_policy + '/'
    tester_builder = DQNTesterBuilder(policy_parent_path, num_learning_episodes, AceZeroDQNNormalizer(), input_dim=4)
    #tester_builder = MultiObjectiveDQNTesterBuilder(policy_path, normalizer=AceZeroDQNNormalizer(), input_dim=4, original_output_dim=5)
    #tester_builder = MultiObjectiveMultiNNDQNTesterBuilder(policy_path, normalizer=AceZeroDQNNormalizer(), input_dim=4, original_output_dim=5, num_rewards=3)
    
    env = AceZeroEnvironment(scenario_name)
    #env.actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)', \
    #               'set_heading(30)', 'set_heading(-30)']
    #env.actions = ['no_command', 'set_heading(30)', 'set_heading(-30)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']

    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(AceZeroBlueRedResultLogger(0.5))
    testing.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=num_trials, num_episodes=num_episodes, num_steps=num_steps)    