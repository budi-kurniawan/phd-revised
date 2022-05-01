#!/usr/bin/env python3
import sys
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000
from rl2020.activity.learning import Learning
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.listener.acezero_random_position_initializer_in_square import AceZeroRandomPositionInitializerInSquare
from rl2020 import agent_builder
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
from rl2020.listener.impl.basic_functions import BasicFunctions
from rl2020.agent_builder.impl.d2dspl_actor_critic_traces_agent_builder import D2DSPLActorCriticTracesAgentBuilder
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.file_log_listener import FileLogListener
from rl2020.listener.impl.policy_maker import PolicyMaker

if __name__ == '__main__':
    init_pos = '001'
    code = 'A' # A=2000
    max_num_samples_for_classifier = 2000 #4000 #3000 #200 #300 #500 #1000 #1500 #2000
    scenario_name = 'basic-' + init_pos + '.json'
    results_name = 'd2dspl-ac-' + init_pos
    out_path = 'rl2020_results/d2dspl-100K/' + code + '/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 100_000
    max_steps_per_episode = 700; chart_offset = 0.5
    milestone_episodes = []
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
        
    env = AceZeroEnvironment(scenario_name)
    agent_builder = D2DSPLActorCriticTracesAgentBuilder(len(env.actions), AceZeroDiscretizer14000(), max_num_samples_for_classifier, 
            AceZeroDQNNormalizer(), milestone_episodes)
    learning = Learning()
    chart_offset = 0.5
    #learning.add_listener(BasicFunctions(chart_offset=0.5, top_n=2, min_recorded_reward=0.1))
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    milestone_episodes = [] #, 200_000, 250_000, 300_000, 400_000]
    learning.add_listener(PolicyMaker(2, 0.1, milestone_episodes));

    learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    #learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)