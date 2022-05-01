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
from rl2020.env.acezero.tester_builder.acezero_actor_critic_multi_policy_tester_builder_001 import AceZeroActorCriticMultiPolicyTesterBuilder001
from rl2020.env.acezero.tester_builder.acezero_actor_critic_multi_policy_tester_builder_002 import AceZeroActorCriticMultiPolicyTesterBuilder002

if __name__ == '__main__':
    """ 
    1. Change the results_name
    2. Change the policy_path. For baseline, it could be anything as it will not be used, but it must exist
    3. Pass an AceZero tester to add_listener, e.g. AceZeroBasicTestA, AceZeroBasicTestB, AceZeroBasicTestC or AceZeroComplexTest()
    """
    scenario_name = 'dummy.json' # could use anything as long as it exists. Does not make a difference in results
    start_trial = 0; num_trials = 10; num_episodes = 200; num_steps = 700    
    results_name = 'ac-mp-001-100000-basic-a'
    results_name = 'ac-mp-002-100000-basic-a'
    results_name = 'ac-mp-003-100000-basic-a'
    out_path = 'rl2020_test_results/' + results_name
    p = 'rl2020_results/ac-so/'
    env = AceZeroEnvironment(scenario_name)
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #activity.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    #activity.add_listener(AceZeroComplexTest())
    
    for trial in range(start_trial, start_trial + num_trials):
        # mp-002, all 5 policies
        # policy_paths = ['rl2020_results/ac-00' + str(x+1) + '/policy0' + str(trial) + '-100000.p' for x in range(5)]
        # mp-003, first 3 policies
        policy_paths = [p + 'ac-00' + str(x+1) + '/policy0' + str(trial) + '-100000.p' for x in range(3)]
        #tester_builder = AceZeroActorCriticMultiPolicyTesterBuilder001(policy_paths, AceZeroDiscretizer14000())
        tester_builder = AceZeroActorCriticMultiPolicyTesterBuilder002(policy_paths, AceZeroDiscretizer14000())
        testing.test(env, out_path, tester_builder=tester_builder, start_trial=trial, num_trials=1, num_episodes=num_episodes, 
                num_steps=num_steps)