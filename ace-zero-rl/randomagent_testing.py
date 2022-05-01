#!/usr/bin/env python3
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.tester_builder.impl.random_tester_builder import RandomTesterBuilder
from rl2020.activity.testing import Testing
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA

if __name__ == '__main__':
    scenario_name = 'dummy.json'
    out_path = 'rl2020_test_results/random-agent-basic-a'
    start_trial = 0; num_trials = 10; num_episodes = 200; num_steps = 700    
    num_actions = 5
    tester_builder = RandomTesterBuilder(num_actions)
    
    env = AceZeroEnvironment(scenario_name)
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    testing.add_listener(AceZeroBasicTestA())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=num_trials, num_episodes=num_episodes, 
                num_steps=num_steps)