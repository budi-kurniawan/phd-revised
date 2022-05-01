#!/usr/bin/env python3
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000
from rl2020.env.acezero.listener.acezero_trajectory_manager import AceZeroTrajectoryManager
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.activity.testing import Testing
from rl2020.tester_builder.impl.mo_actor_critic_tester_builder import MultiObjectiveActorCriticTesterBuilder

if __name__ == '__main__':
    """ 
    1. Change rb
    2. Change num_learning_episodes
    3. Select num_rewards, if necessary
    """
    scenario_name = 'dummy.json' # could use anything as long as it exists. Does not make a difference in results
    #scenario_name = 'blue-stern-conversion-agent.json' #'blue-smart-pursuit-agent.json' #'blue-blue-pursuit-agent.json' #
    rb = 'rb003'
    num_learning_episodes = 200000 #500000
    num_rewards = 3
    results_name = 'ac-mo-random-' + str(num_learning_episodes) + '-' + rb + '-basic-a'
    #results_name = 'baseline-blue-stern-conversion-agent-basic-c2'
    out_path = 'rl2020_test_results/ac-mo/' + results_name
    start_trial = 0; num_trials = 10; num_episodes = 200; num_steps = 700
    #tester_builder = MultiObjectiveActorCriticTesterBuilder3(policy_path, discretizer=AceZeroDiscretizer14000(), num_rewards=2)
    
    env = AceZeroEnvironment(scenario_name)
    testing = Testing()
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(TestResultLogger(0.5))
    #activity.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    #activity.add_listener(AceZeroComplexTest())
    for i in range(start_trial, start_trial + num_trials):
        policy_path = 'rl2021_mo_results/ac-mo/ac-mo-random-200000-' + rb + '/policy0' + str(i) + '-' + str(num_learning_episodes) + '.p'
        print('policy path:', policy_path)
        tester_builder = MultiObjectiveActorCriticTesterBuilder(policy_path, discretizer=AceZeroDiscretizer14000(), num_rewards=num_rewards)
        testing.test(env, out_path, tester_builder=tester_builder, start_trial=i, num_trials=1, num_episodes=num_episodes, num_steps=num_steps)