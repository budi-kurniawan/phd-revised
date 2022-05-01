""" A class representing DQN agents for MORL and multiple neural networks, one for each reward"""

from rl2020.agent.torch_seedable_agent import TorchSeedableAgent
from rl2020.util.util import override
import numpy as np
import torch
from typing import List, Dict
from rl2020.activity.activity_context import ActivityContext
from rl2020.agent.dqn_agent import DQNAgent

__author__ = 'Budi Kurniawan'


class MultiObjectiveMultiNNDQNAgent(TorchSeedableAgent):
    def __init__(self, memory_size, batch_size, dqn_dims, normalizer, reward_builder, seed=None) -> None:
        super().__init__(seed)
        self.output_dim = dqn_dims[-1]
        self.reward_builder = reward_builder
        num_rewards = self.num_rewards = reward_builder.get_num_rewards()
        self.normalizer = normalizer
        self.agents = [DQNAgent(memory_size, batch_size, dqn_dims, normalizer, seed) for _ in range(num_rewards)]

    @override(TorchSeedableAgent)
    def episode_start(self, activity_context: ActivityContext) -> None:
        [agent.episode_start(activity_context) for agent in self.agents]
        min_eps = 0.01
        slope = (min_eps - 1.0) / (activity_context.num_episodes - 1)
        self.current_epsilon = max(slope * activity_context.episode + 1.0, min_eps)
        self.total_redefined_reward = 0
        self.total_rewards = np.zeros(self.num_rewards)
                
    def clean_up(self)->None:
        [agent.clean_up() for agent in self.agents]
                
    def update(self, activity_context: ActivityContext, state:np.ndarray, action: int, reward: List[float], next_state:np.ndarray, terminal: bool, env_data: Dict[str, object]) -> None:
        rewards = self.reward_builder.get_rewards(env_data)
        self.total_rewards = np.add(rewards, self.total_rewards)
        self.total_redefined_reward += np.sum(rewards)
        for i in range(self.num_rewards):
            self.agents[i].update(activity_context, state, action, rewards[i], next_state, terminal, env_data)

    def save_policy(self, path): # used to save a policy that can be used for activity
        for i in range(self.num_rewards):
            path_i = path + '_' + str(i)
            self.agents[i].save_policy(path_i)
        
    def select_action(self, state: np.ndarray) -> int:
        if self.np_random.random() < self.current_epsilon:
            return self.np_random.choice(self.output_dim)
        else:
            normalized_state = state if self.normalizer is None else self.normalizer.normalize(state)
            list_of_q_values = []
            for agent in self.agents:
                agent.dqn.train(mode=False)
                q_values = agent.get_Q(normalized_state).cpu().detach().numpy()
                list_of_q_values.append(q_values)
            sum_of_Qs = np.sum(list_of_q_values, axis=0)
            action = int(np.argmax(sum_of_Qs))            
            return action