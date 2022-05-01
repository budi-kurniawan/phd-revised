#!/usr/bin/env python3
import sys
from rl2020.agent.dqn_agent import DQNAgent
from rl2020.agent.agent import Agent
from rl2020.env.acezero.ace_zero_3d_env import AceZero3DEnvironment
from rl2020.activity.learning import Learning
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.file_log_listener import FileLogListener
from rl2020.listener.impl.policy_maker import PolicyMaker
from rl2020.env.acezero.normalizer.acezero_dqn_3d_normalizer import AceZeroDQN3DNormalizer
from rl2020.env.acezero.listener.acezero_simple_random_3d_position_initializer import AceZeroSimpleRandom3DPositionInitializer
from rl2020.agent_builder.agent_builder import AgentBuilder

class AceZeroDQN3DAgentBuilder(AgentBuilder):
    def create_agent(self, seed, initial_policy_path=None):
        in_dim = 5
        memory_size = 1_000_000; batch_size = 64; dqn_dims = [in_dim, 300, self.num_actions]
        return DQNAgent(memory_size, batch_size, dqn_dims, self.normalizer, self.num_episodes, seed)
    
if __name__ == '__main__':
    scenario_name = 'basic-3d-001.json'
    results_name = 'dqn-3d-001'
    out_path = 'rl2020_results/' + results_name
    start_trial = 0; num_trials = 1; num_episodes = 100_000
    max_steps_per_episode = 700; chart_offset = 0.5
    
    if len(sys.argv) > 1:
        start_trial = int(sys.argv[1])
    
    env = AceZero3DEnvironment(scenario_name)    
    learning = Learning()
    learning.add_listener(ConsoleLogListener())
    learning.add_listener(FileLogListener(chart_offset));
    learning.add_listener(PolicyMaker(10, 0.1));
    learning.add_listener(AceZeroSimpleRandom3DPositionInitializer())
    agent_builder = AceZeroDQN3DAgentBuilder(len(env.actions), normalizer=AceZeroDQN3DNormalizer(), num_episodes=num_episodes)
    learning.learn(env, out_path, start_trial, num_trials, num_episodes, max_steps_per_episode, agent_builder)
