#!/usr/bin/env python3
import sys
from rl2020.agent.d2dsql_agent2 import D2DSQLAgent2
from rl2020.env.acezero.ace_zero_env import AceZeroEnvironment
from rl2020.activity.learning import Learning
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.env.acezero.normalizer.acezero_dqn_normalizer import AceZeroDQNNormalizer
from rl2020.agent_builder.agent_builder import AgentBuilder
from rl2020.listener.impl.basic_functions import BasicFunctions
from rl2020.env.acezero.listener.acezero_random_position_initializer_in_square import AceZeroRandomPositionInitializerInSquare
from rl2020.listener.impl.session_logger import SessionLogger
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.file_log_listener import FileLogListener
from rl2020.listener.impl.policy_maker import PolicyMaker

""" use D2DSQLAgent2 (fixed epsilon of 0.05) instead of D2DSQLAgent """
class AceZeroD2DSQLAgentBuilder(AgentBuilder):
    def create_agent(self, seed, initial_policy_path=None):
        memory_size = 1_000_000; batch_size = 64; dqn_dims = [4, 300, self.num_actions]
        trial = seed
        normalized_training_set_path = normalized_training_set_parent_path + '/d2dspl-normalised_training_set-0' + str(trial) + '-00100000.txt'
        return D2DSQLAgent2(normalized_training_set_path, target_loss, memory_size, batch_size, dqn_dims, self.normalizer, seed)

if __name__ == '__main__':
    test_number = '002'
    edition = 'A'
    scenario_name = 'basic-' + test_number + '.json'
    results_name = edition + '/d2dsql2-100000-' + test_number
    normalized_training_set_parent_path = 'rl2020_results/d2dspl/' + edition + '/d2dspl-ac-' + test_number
    out_path = 'rl2020_results/d2dsql2/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 20_000;
    target_loss = 0.01 #0.001
    max_steps_per_episode = 700; chart_offset = 0.5
    env_reward_builder = None
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZeroEnvironment(scenario_name, env_reward_builder)
    description = 'd2dsql agent. training set from ' + normalized_training_set_parent_path + \
            '/d2dspl-normalised_training_set-0x-00100000.txt\n target_loss: ' + str(target_loss)
    learning = Learning()
    milestone_episodes = [10_000, 11_000, 12_000, 13_000, 14_000, 15_000, 16_000, 17_000, 18_000, 19_000]
    chart_offset = 0.5
    #learning.add_listener(BasicFunctions(chart_offset=0.5, top_n=2, min_recorded_reward=0.1))
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    learning.add_listener(PolicyMaker(2, 0.1, milestone_episodes));

    #learning.add_listener(BasicFunctions(chart_offset=chart_offset, top_n=2, min_recorded_reward=0.1, milestone_episodes=milestone_episodes))
    learning.add_listener(SessionLogger(description))
    learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    #learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    agent_builder = AceZeroD2DSQLAgentBuilder(len(env.actions), normalizer=AceZeroDQNNormalizer(), agent_load_path=out_path)
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)