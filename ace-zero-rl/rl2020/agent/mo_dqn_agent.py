""" A class representing MO DQN agents. An instance uses a single NN. 
    This class is similar to DQNAgent except that the number of output nodes is multiplied by the number of rewards 
"""

from typing import Dict
from rl2020.util.util import override
from rl2020.agent.dqn_agent import DQNAgent
import numpy as np
import torch
from rl2020.activity.activity_context import ActivityContext

__author__ = 'bkurniawan'

class MultiObjectiveDQNAgent(DQNAgent):
    def __init__(self, memory_size, batch_size, dqn_dims, normalizer, reward_builder, seed=None) -> None:
        self.num_rewards = reward_builder.get_num_rewards()
        self.original_output_dim = dqn_dims[-1]
        dqn_dims[-1] *= self.num_rewards
        super().__init__(memory_size, batch_size, dqn_dims, normalizer, seed)
        self.reward_builder = reward_builder

    @override(DQNAgent)
    def episode_start(self, activity_context: ActivityContext):
        super().episode_start(activity_context)
        self.total_redefined_reward = 0
        self.total_rewards = np.zeros(self.num_rewards)
        
    @override(DQNAgent)
    def update(self, activity_context: ActivityContext, state:np.ndarray, action: int, reward: float, next_state:np.ndarray, 
               terminal: bool, env_data: Dict[str, object]) -> None:
        rewards = self.reward_builder.get_rewards(env_data)
        self.total_rewards = np.add(rewards, self.total_rewards)
        self.total_redefined_reward += np.sum(rewards)
        self.add_sample(state, action, rewards, next_state, terminal)
        self.train()
        
    @override(DQNAgent)
    def select_action(self, state: np.ndarray) -> int:
        if self.np_random.random() < self.current_epsilon:
            return self.np_random.choice(self.original_output_dim)
        else:
            self.dqn.train(mode=False)
            if self.normalizer is not None:
                q_values = self.get_Q(self.normalizer.normalize(state))
            else:
                q_values = self.get_Q(state)
            """ scores.data is of type tensor(1, dim_out), len(scores.data) = 1
                scores.data[0] of type tensor(dim_out), len(scores.data[0]) = dim_out
            """
            individual_scores = torch.split(q_values.data[0], self.original_output_dim)
            sum_of_scores = torch.zeros(self.original_output_dim)
            for i in range(len(individual_scores)):
                sum_of_scores += individual_scores[i]
            return int(torch.argmax(sum_of_scores))

    @override(DQNAgent)
    def train(self) -> None:
        if len(self.memory) <= self.batch_size:
            return
        minibatch = self.memory.pop(self.batch_size)
        normalized_states = np.vstack([x.state for x in minibatch])
        actions = np.array([x.action for x in minibatch])
        rewards = np.array([x.reward for x in minibatch])
        normalized_next_states = np.vstack([x.next_state for x in minibatch])
        done = np.array([x.done for x in minibatch])

        Q_predict = self.get_Q(normalized_states)
        #print('q_predict', Q_predict)
        Q_target = Q_predict.clone().data.numpy()
        """ Q_target is an numpy.ndarray of size (len(minibatch), num_actions).
            At this point Q_target[np.arange(len(Q_target)), actions]) is a 1-dim array of size len(minibatch) and each element is selected from
            the corresponding row. Which cell in the row is used depends on the value of the corresponding actions
            For example, suppose len(minibatch) = 2 and num_actions=3 and Q_target is [[1, 2, 3], [4, 5, 6]] and actions = [1, 0]
            Q_target[np.arange(len(Q_target)), actions]) is then a 1-dim array of size len(minibatch) -> [2, 4], 
            where 2 is taken from the 1st element of [1,2,3] and 4 from the zeroth of [4,5,6].
            However, more importantly here, Q_target[np.arange(len(Q_target)), actions]) represents locations whose values are to be replaced
        """
        Q_predict_next = self.get_Q(normalized_next_states).data.numpy()
        for row in range(len(minibatch)):
            action = actions[row]
            for reward_no in range(self.num_rewards):
                # rewards' shape is (minibatch, num_rewards)
                Q_predict_next_subset = []
                offset = reward_no * self.original_output_dim
                for i in range(self.original_output_dim):
                    Q_predict_next_subset.append(Q_predict_next[row][i + offset])
                reward = rewards[row][reward_no]
                Q_target[row][action + reward_no * self.original_output_dim] = reward + self.gamma * np.max(Q_predict_next_subset) * (~done[row])
        Q_target = torch.Tensor(Q_target)
        """
            Exactly one cell in each row in Q_target has been updated. In other words, the nth row of Q_predict and 
            the nth row of Q_target differs by one value
        """
        return self._train(Q_predict, Q_target)