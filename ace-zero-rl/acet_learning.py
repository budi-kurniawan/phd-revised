#!/usr/bin/env python3
import sys
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000
from rl2020.activity.learning import Learning
from rl2020.listener.impl.policy_maker import PolicyMaker
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.file_log_listener import FileLogListener
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.listener.acezero_random_position_initializer_in_square import AceZeroRandomPositionInitializerInSquare
from rl2020.listener.impl.policy_loader import PolicyLoader
from rl2020.agent_builder.impl.actor_critic_traces_agent_builder import ActorCriticTracesAgentBuilder
from rl2020 import agent_builder
from rl2020.env.acezero.env_reward_builder.acezero_env_reward_builder_002 import AceZeroEnvironmentRewardBuilder002
from rl2020.env.acezero.env_reward_builder.acezero_env_reward_builder_003 import AceZeroEnvironmentRewardBuilder003

if __name__ == '__main__':
    scenario_name = 'basic-005.json'
    #scenario_name = 'red-smart-pursuit-agent.json'
    #results_name = 'ac-random-001-smart_pursuit'
    results_name = 'ac-005'
    #results_name = 'ac-random'
    out_path = 'rl2020_results/ac-so-500K/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 200_000
    max_steps_per_episode = 700; chart_offset = 0.5
    env_reward_builder = None #AceZeroEnvironmentRewardBuilder003()
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
        
    env = AceZeroEnvironment(scenario_name, env_reward_builder)
    #env.actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)', \
    #               'set_heading(30)', 'set_heading(-30)']
    #env.actions = ['no_command', 'set_heading(30)', 'set_heading(-30)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']
    agent_builder = ActorCriticTracesAgentBuilder(len(env.actions), discretizer=AceZeroDiscretizer14000())
    learning = Learning()
    learning.add_listener(PolicyLoader())
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    milestone_episodes = [50_000, 100_000] #, 200_000, 250_000, 300_000, 400_000]
    learning.add_listener(PolicyMaker(2, 0.1, milestone_episodes));
    learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    #learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)
