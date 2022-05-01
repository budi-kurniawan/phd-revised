#!/usr/bin/env python3
import sys
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.listener.acezero_trajectory_manager import AceZeroTrajectoryManager
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.activity.testing import Testing
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
sys.path.insert(0, "../spyrl")
from spyrl.tester_builder.impl.ppo_tester_builder import PPOTesterBuilder

if __name__ == '__main__':
    """
        1. Select a results_name
        2. Select a policy_path
        3. Select a tester_builder
        Note: No need to worry about scenario_name as long as it does exist
    """
    
    scenario_name = 'dummy.json' # does not matter
    code = 'ppo700-002'
    code = 'ppo4K-random'
    results_name = code + '-20000-basic-a'
    out_path = 'rl2020_test_results/ppo-so/' + results_name
    start_trial = 5; num_trials = 5; num_episodes = 1000; num_steps = 700
    
    policy_parent_path = 'rl2020_results/ppo-so/' + code + '/'; num_learning_episodes = 20_000 #20_000
    normaliser = AceZeroDQNNormalizer()
    tester_builder = PPOTesterBuilder(policy_parent_path, num_learning_episodes, normaliser)
    
    env = AceZeroEnvironment(scenario_name)
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #testing.add_listener(AceZeroTrajectoryManager())

    testing.add_listener(AceZeroBasicTestA())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=num_trials, num_episodes=num_episodes, 
                num_steps=num_steps)
