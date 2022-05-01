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
    1. Assign results_name
    2. Assign policy_parent_path
    3. Assign num_learning_episodes
    """
    results_name = 'ac-random-1000000-complex-a'
    #results_name = 'ac-004-100000-complex-a'
    out_path = 'rl2020_test_results_complex/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 4; num_steps = 1000    
    policy_parent_path = 'rl2020_results/ac-random-001/'; num_learning_episodes = 1000_000
    #policy_parent_path = 'rl2020_results/ac-004/'; num_learning_episodes = 100_000
    tester_builder = ActorCriticTesterBuilder(policy_parent_path, num_learning_episodes, AceZeroDiscretizer14000())    
    env = AceZeroEnvironment('dummy.json')
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    testing.add_listener(AceZeroTrajectoryManager())
    #testing.add_listener(AceZeroBasicTestA())
    testing.add_listener(AceZeroComplexTest())
    testing.test(env, out_path, tester_builder=tester_builder, start_trial=start_trial, num_trials=1, num_episodes=num_episodes, 
        num_steps=num_steps)