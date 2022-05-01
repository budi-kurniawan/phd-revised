"""
This class represents an multiobjective Q-learning agent which contains multiple QLearning with traces agents
"""
import numpy as np
import pickle
from rl2020.agent.seedable_agent import SeedableAgent
from typing import Dict
from rl2020.agent.actor_critic_traces_agent import ActorCriticTracesAgent
from rl2020.util.util import override
from rl2020.activity.activity_context import ActivityContext

__author__ = 'bkurniawan'

class MultiObjectiveActorCriticTracesAgent(SeedableAgent):
    
    def __init__(self, num_actions, discretizer, reward_builder, seed=None) -> None:
        super().__init__(seed)
        self.num_actions = num_actions
        self.discretizer = discretizer
        self.num_rewards = reward_builder.get_num_rewards()
        self.reward_builder = reward_builder
        self.agents = [ActorCriticTracesAgent(num_actions, discretizer, seed) for _ in range(self.num_rewards)]
        self.actions = np.arange(num_actions)

    @override(SeedableAgent)
    def episode_start(self, activity_context: ActivityContext)->None:
        [agent.episode_start(activity_context) for agent in self.agents]
        self.total_redefined_reward = 0
        self.total_rewards = np.zeros(self.num_rewards)

    def select_action(self, state) -> int:
#         if self.np_random.random() < 0.1: # use fixed epsilon here
#             return self.np_random.choice(self.num_actions)
#         else:
#             discrete_state = self.discretizer.discretize(state)
#             q_values_list = [agent.theta[discrete_state] for agent in self.agents] # list of x ndarrays where x = num_rewards
#             sum_of_q_values = np.sum(q_values_list, axis=0)
#             return np.argmax(sum_of_q_values)
        discrete_state = self.discretizer.discretize(state)
        q_values_list = [agent.theta[discrete_state] for agent in self.agents] # list of x ndarrays where x = num_rewards
        sum_of_q_values = np.sum(q_values_list, axis=0)
        prob = self.softmax(sum_of_q_values)
        return self.np_random.choice(self.actions, p=prob)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def update(self, activity_context: ActivityContext, state:np.ndarray, action: int, reward: float, next_state:np.ndarray, 
               terminal: bool, env_data: Dict[str, object]) -> None:
        rewards = self.reward_builder.get_rewards(env_data)
        self.total_rewards = np.add(rewards, self.total_rewards)
        self.total_redefined_reward += np.sum(rewards)
        for i in range(self.num_rewards):
            self.agents[i].update(activity_context, state, action, rewards[i], next_state, terminal, env_data)

    def save_policy(self, path): # used to save a policy that can be used for activity
        for i in range(self.num_rewards):
            path_i = path + '_' + str(i)
            file = open(path_i, 'wb')
            pickle.dump(self.agents[i].theta, file)
            file.close()
