#!/usr/bin/env python3
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000
from rl2020.env.acezero.listener.acezero_basic_test_c import AceZeroBasicTestC
from rl2020.env.acezero.listener.acezero_trajectory_manager import AceZeroTrajectoryManager
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.env.acezero.listener.acezero_basic_test_b import AceZeroBasicTestB
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.env.acezero.listener.acezero_complex_test import AceZeroComplexTest
from rl2020.activity.testing import Testing
from rl2020.tester_builder.impl.mo_actor_critic_tester_builder import MultiObjectiveActorCriticTesterBuilder
from rl2020.tester_builder.impl.mo_actor_critic_tester_builder2 import MultiObjectiveActorCriticTesterBuilder2
from rl2020.tester_builder.impl.mo_actor_critic_tester_builder3 import MultiObjectiveActorCriticTesterBuilder3
from rl2020.env.acezero.listener.acezero_blue_red_result_logger import AceZeroBlueRedResultLogger
from rl2020.listener.impl.session_logger import SessionLogger

if __name__ == '__main__':
    """ 
    1. Change rb
    2. Change agent_type
    """
    
    rb = 'rb016'
    agent_type = 'pure-pursuit'
    agent_type = 'smart-pursuit'
    agent_type = 'stern-conversion'
    #agent_type = 'restricted-pure-pursuit'
    #agent_type = 'restricted-smart-pursuit'
    #agent_type = 'restricted-stern-conversion'
    num_learning_episodes = 500000
    description = 'ac-mo-random-' + str(num_learning_episodes) + '-' + rb + ' vs red_' + agent_type + ' (Basic A)'
    scenario_name = 'red-' + agent_type + '-agent.json'

    results_name = 'ac-mo-random-' + str(num_learning_episodes) + '-' + rb + '-red-' + agent_type + '-basic-a'
    out_path = 'rl2020_test_results/ac-mo/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 200; num_steps = 700
    num_rewards = 2
        
    env = AceZeroEnvironment(scenario_name)
    testing = Testing()
    testing.add_listener(SessionLogger(description))
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(AceZeroBlueRedResultLogger(0.5))
    testing.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBasicTestA())
    #activity.add_listener(AceZeroComplexTest())
    
    for trial in range(start_trial, start_trial + num_trials):
        policy_path = 'rl2021_mo_results/ac-mo/ac-mo-random-' + str(num_learning_episodes) + '-' + rb + '/policy0' + str(trial) + '-' + str(num_learning_episodes) + '.p'
        tester_builder = MultiObjectiveActorCriticTesterBuilder(policy_path, discretizer=AceZeroDiscretizer14000(), num_rewards=num_rewards)
        testing.test(env, out_path, tester_builder=tester_builder, start_trial=trial, num_trials=1, num_episodes=num_episodes, num_steps=num_steps)