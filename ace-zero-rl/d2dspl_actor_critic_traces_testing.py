#!/usr/bin/env python3
from rl2020.activity.testing import Testing
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.env.acezero.listener.acezero_basic_test_b import AceZeroBasicTestB
from rl2020.env.acezero.listener.acezero_basic_test_c import AceZeroBasicTestC
from rl2020.env.acezero.listener.acezero_trajectory_manager import AceZeroTrajectoryManager
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.tester_builder.impl.d2dspl_actor_critic_traces_tester_builder import D2DSPLActorCriticTracesTesterBuilder

if __name__ == '__main__':
    """
        1. Change edition
        2. Change test_name
    """
    
    scenario_name = 'dummy.json' # does not matter
    edition = 'A'
    test_name = 'random'
    results_name = 'd2dspl-ac-' + test_name + '-100000-basic-a'
    out_path = 'rl2020_test_results/d2dspl/' + edition + '/' + results_name
    start_trial = 0; num_trials = 10; num_episodes = 1000; num_steps = 700
    policy_parent_path = 'rl2020_results/d2dspl/' + edition + '/d2dspl-ac-' + test_name + '/'; 
    num_learning_episodes = 100_000
    tester_builder = D2DSPLActorCriticTracesTesterBuilder(policy_parent_path, num_learning_episodes, AceZeroDQNNormalizer())
    
    env = AceZeroEnvironment(scenario_name)
    #env.actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)', \
    #               'set_heading(30)', 'set_heading(-30)']
    #env.actions = ['no_command', 'set_heading(30)', 'set_heading(-30)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']

    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #activity.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=num_trials, num_episodes=num_episodes, 
                 num_steps=num_steps)