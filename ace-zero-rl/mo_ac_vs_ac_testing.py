#!/usr/bin/env python3
from rl2020.env.acezero.ace_zero_rl_vs_rl_env import AceZeroRLVsRLEnvironment
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000
from rl2020.env.acezero.listener.acezero_basic_test_c import AceZeroBasicTestC
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.listener.acezero_trajectory_manager import AceZeroTrajectoryManager
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.test_result_logger import TestResultLogger
from rl2020.env.acezero.listener.acezero_before_reset_positioning import AceZeroBeforeResetPositioning
from rl2020.env.acezero.listener.acezero_complex_test import AceZeroComplexTest
from rl2020.env.acezero.listener.acezero_step_logger import AceZeroStepLogger
from rl2020.activity.testing import Testing
from rl2020.listener.impl.session_logger import SessionLogger
from rl2020.env.acezero.listener.acezero_blue_red_result_logger import AceZeroBlueRedResultLogger
from rl2020.tester.actor_critic_tester import ActorCriticTester
from rl2020.tester.mo_actor_critic_tester import MultiObjectiveActorCriticTester

if __name__ == '__main__':
    mo_agent = 'rb016'
    viper_num_learning_episodes = 200000
    cobra_num_learning_episodes = 200000
    scenario_name = 'rl_vs_rl.json' # rl_vs_rl.json must not have initials
    #results_name = 'ac-mo-random-500000-rb013-vs-ac-mo-random-500000-rb013-basic-a'
    results_name = 'ac-mo-random-' + str(viper_num_learning_episodes) + '-' + mo_agent + \
        '-vs-ac-random-' + str(cobra_num_learning_episodes) + '-basic-a'
    out_path = 'rl2020_test_results/' + results_name
    description = 'RL vs RL. ' + results_name
    start_trial = 0; num_trials = 10; start_episode = 1; num_episodes = 200; num_steps = 700
    discretizer = AceZeroDiscretizer14000()
    num_rewards = 2

    testing = Testing()
    testing.add_listener(SessionLogger(description))
    testing.add_listener(ConsoleLogListener())
    testing.add_listener(AceZeroBlueRedResultLogger(0.5))
    #testing.add_listener(AceZeroTrajectoryManager())
    testing.add_listener(AceZeroBeforeResetPositioning()) # Must not have AceZeroBasicTestA
    #testing.add_listener(AceZeroStepLogger())
    #activity.add_listener(AceZeroComplexTest())
    for trial in range(start_trial, start_trial + num_trials):
        viper_policy_path = 'rl2020_results/ac-mo/ac-mo-random-001-500000-' + mo_agent + '/policy0' + str(trial) + '-' + str(viper_num_learning_episodes) + '.p'
        viper_tester = MultiObjectiveActorCriticTester(viper_policy_path, discretizer=discretizer, num_rewards=num_rewards, id='viper')
#         viper_policy_path = 'rl2020_results/ac-random-001/policy0' + str(trial) + '-1000000.p'
#         viper_tester = ActorCriticTester(viper_policy_path, discretizer=discretizer)        
#         cobra_policy_path = 'rl2020_results/ac-mo-random-001-500000-rb013/policy0' + str(trial) + '-500000.p'
#         cobra_tester = MultiObjectiveActorCriticTester(cobra_policy_path, discretizer=discretizer, num_rewards=num_rewards, id='cobra')
        cobra_policy_path = 'rl2020_results/ac-so/ac-random-001/policy0' + str(trial) + '-' + str(cobra_num_learning_episodes) + '.p'
        cobra_tester = ActorCriticTester(cobra_policy_path, discretizer=discretizer)
        env = AceZeroRLVsRLEnvironment(scenario_name, cobra_tester)
        testing.test(env, out_path, tester=viper_tester, start_trial=trial, start_episode=start_episode, num_episodes=num_episodes, num_steps=num_steps)