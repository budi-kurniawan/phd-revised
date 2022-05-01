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
from rl2020.agent_builder.impl.q_learning_traces_agent_builder import QLearningTracesAgentBuilder
from rl2020 import agent_builder

if __name__ == '__main__':
    scenario_name = 'dummy.json' #'basic-005.json'
    results_name = 'ql-random'
    out_path = 'rl2020_results/ql-so-200K/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 200_000
    max_steps_per_episode = 700; chart_offset = 0.5
    description = 'description of this learning'
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
        
    env = AceZeroEnvironment(scenario_name)
    learning = Learning()
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    milestone_episodes = [100_000]
    learning.add_listener(PolicyMaker(2, 0.1, milestone_episodes));
    
    #learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    agent_builder = QLearningTracesAgentBuilder(len(env.actions), discretizer=AceZeroDiscretizer14000())
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)
