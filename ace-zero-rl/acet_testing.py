#!/usr/bin/env python3
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000
from rl2020.env.acezero.listener.acezero_basic_test_c import AceZeroBasicTestC
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.listener.acezero_trajectory_manager import AceZeroTrajectoryManager
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.env.acezero.listener.acezero_basic_test_b import AceZeroBasicTestB
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.env.acezero.listener.acezero_complex_test import AceZeroComplexTest
from rl2020.activity.testing import Testing
from rl2020.tester_builder.impl.actor_critic_tester_builder import ActorCriticTesterBuilder
from rl2020.env.acezero.tester_builder.acezero_actor_critic_multi_policy_tester_builder_001 import AceZeroActorCriticMultiPolicyTesterBuilder001
from rl2020.env.acezero.tester_builder.acezero_actor_critic_multi_policy_tester_builder_002 import AceZeroActorCriticMultiPolicyTesterBuilder002

if __name__ == '__main__':
    """ 
    1. Change the scenario_name. For activity, use basic-00x.json. For baseline, use blue-smart-pursuit-agent.json etc
    2. Change the results_name
    3. Change the policy_path. For baseline, it could be anything as it will not be used, but it must exist
    4. Pass an AceZero tester to add_listener, e.g. AceZeroBasicTestA, AceZeroBasicTestB, AceZeroBasicTestC or AceZeroComplexTest()
    """
    scenario_name = 'dummy.json' # could use anything as long as it exists. Does not make a difference in results
    #scenario_name = 'blue-stern-conversion-agent.json' #'blue-smart-pursuit-agent.json' #'blue-blue-pursuit-agent.json' #

    test_code = '005'
    #test_code = 'random'
    num_learning_episodes = 200_000
    results_name = 'ac-' + test_code + '-' + str(num_learning_episodes).zfill(6) + '-basic-a'
    #results_name = 'baseline-blue-stern-conversion-agent-basic-c2'
    out_path = 'rl2020_test_results/' + results_name
    start_trial = 0; num_trials = 10; num_episodes = 200; num_steps = 700
    
    policy_parent_path = 'rl2020_results/ac-so-500K/ac-' + test_code + '/'; 
    tester_builder = ActorCriticTesterBuilder(policy_parent_path, num_learning_episodes, AceZeroDiscretizer14000())
    
    env = AceZeroEnvironment(scenario_name)
    #env.actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)', \
    #               'set_heading(30)', 'set_heading(-30)']
    #env.actions = ['no_command', 'set_heading(30)', 'set_heading(-30)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']

    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #activity.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    #activity.add_listener(AceZeroComplexTest())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=num_trials, num_episodes=num_episodes, 
                num_steps=num_steps)