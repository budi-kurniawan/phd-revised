#!/usr/bin/env python3
import sys
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.activity.testing import Testing
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.tester_builder.impl.mo_dqn_tester_builder import MultiObjectiveDQNTesterBuilder

if __name__ == '__main__':
    scenario_name = 'dummy.json' # could use anything as long as it exists. Does not make a difference in results
    rb = 'rb003'
    num_learning_episodes = 20000
    num_rewards = 3
    results_name = 'dqn-mo-shared-random-' + str(num_learning_episodes) + '-' + rb + '-basic-a'
    #results_name = 'baseline-blue-stern-conversion-agent-basic-c2'
    out_path = 'rl2020_test_results/dqn-mo-shared/' + results_name
    start_trial = 0; num_trials = 5; num_episodes = 200; num_steps = 700
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZeroEnvironment(scenario_name)
    normalizer = None
    input_dim = 4
    original_output_dim = 5
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #activity.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    for i in range(start_trial, start_trial + num_trials):
        policy_path = 'rl2021_mo_results/dqn-mo-shared/dqn-mo-shared-random-20000-' + rb + '/policy0' + str(i) + '-' + str(num_learning_episodes) + '.p'
        print('policy path:', policy_path)
        tester_builder = MultiObjectiveDQNTesterBuilder(policy_path, normalizer=normalizer, input_dim=input_dim, original_output_dim=original_output_dim)
        testing.test(env, out_path, tester_builder=tester_builder, start_trial=i, num_trials=1, num_episodes=num_episodes, num_steps=num_steps)
    