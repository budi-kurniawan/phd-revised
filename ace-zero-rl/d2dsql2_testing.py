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
        This is a copy of dqn_testing.py
        1. Select a test_number
        2. Select an edition
    """    
    scenario_name = 'dummy.json' # does not matter
    test_number = '002'
    edition = 'A'
    num_learning_episodes = 10_000
    results_name = 'd2dsql2-ac-100000-' + test_number + '-' + str(num_learning_episodes).zfill(6) + '-basic-a'
    out_path = 'rl2020_test_results/d2dsql2/' + edition + '/' + results_name
    start_trial = 0; num_trials = 10; num_episodes = 1000; num_steps = 700
    
    policy_parent_path = 'rl2020_results/d2dsql2/' + edition + '/d2dsql2-100000-' + test_number + '/'; 
    tester_builder = DQNTesterBuilder(policy_parent_path, num_learning_episodes, AceZeroDQNNormalizer(), input_dim=4)
    
    env = AceZeroEnvironment(scenario_name)
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #activity.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=num_trials, num_episodes=num_episodes, 
                num_steps=num_steps)