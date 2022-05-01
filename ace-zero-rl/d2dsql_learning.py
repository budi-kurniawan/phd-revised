#!/usr/bin/env python3
import sys
from rl2020.agent.d2dsql_agent import D2DSQLAgent
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

class AceZeroD2DSQLAgentBuilder(AgentBuilder):
    def create_agent(self, seed, initial_policy_path=None):
        memory_size = 1_000_000; batch_size = 64; dqn_dims = [4, 300, self.num_actions]
        trial = seed
        normalized_training_set_path = normalized_training_set_parent_path + '/d2dspl-normalised_training_set-0' + str(trial) + '-00050000.txt'
        return D2DSQLAgent(normalized_training_set_path, target_loss, memory_size, batch_size, dqn_dims, self.normalizer, seed)
    
if __name__ == '__main__':
    test_number = '001'
    edition = 'B'
    scenario_name = 'basic-' + test_number + '.json'
    results_name = edition + '/d2dsql-001'
    normalized_training_set_parent_path = 'rl2020_results/d2dspl/' + edition + '/d2dspl-ac-' + test_number
    out_path = 'rl2020_results/d2dsql/' + results_name
    start_trial = 1; num_trials = 1; num_episodes = 10_000;
    target_loss = 0.01 #0.001
    max_steps_per_episode = 700; chart_offset = 0.5
    env_reward_builder = None
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZeroEnvironment(scenario_name, env_reward_builder)
    #env.actions = ['no_command', 'set_heading(10)', 'set_heading(-10)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)', \
    #               'set_heading(30)', 'set_heading(-30)']
    #env.actions = ['no_command', 'set_heading(30)', 'set_heading(-30)', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']
    
    description = 'd2dsql agent. training set from ' + normalized_training_set_parent_path + '/d2dspl-normalised_training_set-0x-00050000.txt\n' + \
            'target_loss: ' + str(target_loss)
    learning = Learning()
    chart_offset = 0.5
    #learning.add_listener(BasicFunctions(chart_offset=0.5, top_n=2, min_recorded_reward=0.1))
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    milestone_episodes = [] #, 200_000, 250_000, 300_000, 400_000]
    learning.add_listener(PolicyMaker(2, 0.1, []));
    #learning.add_listener(BasicFunctions(chart_offset=chart_offset, top_n=10, min_recorded_reward=0.1))
    learning.add_listener(SessionLogger(description))
    learning.add_listener(AceZeroSimpleRandomPositionInitializer())
    #learning.add_listener(AceZeroRandomPositionInitializerInSquare())
    agent_builder = AceZeroD2DSQLAgentBuilder(len(env.actions), normalizer=AceZeroDQNNormalizer(), agent_load_path=out_path)
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)