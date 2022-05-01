#!/usr/bin/env python3
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

if __name__ == '__main__':
    """
        1. Select a results_name
        2. Select a policy_path
        3. Select a tester_builder
        Note: No need to worry about scenario_name as long as it does exist
    """
    
    scenario_name = 'dummy.json' # does not matter
    #scenario_name = 'blue-pure-pursuit-agent.json'
    #results_name = 'dqn-mo-001-erb003-20000-basic-a'
    #results_name = 'dqn-momnn-random-001-50000-rb013-basic-a'
    #results_name = 'dqn-mo-random-001-50000-rb013-basic-a'
    #results_name = 'dqn-wtn-c10-001-20000-basic-a'
    #results_name = 'double-dqn-001-19970-basic-a'
    results_name = 'dqn-random-20000-basic-a'
    #results_name = 'dqn-wtn-c700-random-20000-basic-a'
    #results_name = 'double-dqn-random-20000-basic-a'
    out_path = 'rl2020_test_results/' + results_name
    start_trial = 0; num_trials = 10; num_episodes = 1000; num_steps = 700
    
    policy_parent_path = 'rl2020_results/dqn-so/dqn-random/'; num_learning_episodes = 20_000 #20_000
    tester_builder = DQNTesterBuilder(policy_parent_path, num_learning_episodes, AceZeroDQNNormalizer(), input_dim=4)
    #tester_builder = MultiObjectiveDQNTesterBuilder(policy_path, normalizer=AceZeroDQNNormalizer(), input_dim=4, original_output_dim=5)
    #tester_builder = MultiObjectiveMultiNNDQNTesterBuilder(policy_path, normalizer=AceZeroDQNNormalizer(), input_dim=4, original_output_dim=5, num_rewards=2)
    
    env = AceZeroEnvironment(scenario_name)
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #activity.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=num_trials, num_episodes=num_episodes, 
                num_steps=num_steps)
