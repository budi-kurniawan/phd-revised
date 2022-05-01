from rl2020.util.util import override
from rl2020.activity.activity_context import ActivityContext
from rl2020.agent.torch_seedable_agent import TorchSeedableAgent
from rl2020.agent.dqn.dqn import DQN, ReplayMemory
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict
from rl2020.agent.dqn_agent import DQNAgent

""" A class representing DQN agents on GPU """
""" Not Finished yet. See
 https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html#q-network
 https://github.com/pytorch/tutorials/blob/master/intermediate_source/reinforcement_q_learning.py

https://towardsdatascience.com/pytorch-switching-to-the-gpu-a7c0b21e8a99
"""
__author__ = 'bkurniawan'

class DQNAgentOnGPU(DQNAgent):
    def __init__(self, memory_size, batch_size, dqn_dims, normalizer, seed=None) -> None:
        super().__init__(memory_size, batch_size, dqn_dims, normalizer, seed)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dqn.to(self.device)
        print('DQNAgentOnGPU. device:', self.device)
        print('dqn.is_cuda :', self.dqn.is_cuda)

    @override(TorchSeedableAgent)
    def update(self, activity_context: ActivityContext, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, terminal: bool, env_data: Dict[str, object]) -> None:
        self.add_sample(state, action, reward, next_state, terminal)
        self.train()
        
    @override(TorchSeedableAgent)
    def select_action(self, state: np.ndarray) -> int:
        if self.np_random.random() < self.current_epsilon:
            return self.np_random.choice(self.output_dim)
        else:
            self.dqn.train(mode=False)
            q_values = self.get_Q(state) if self.normalizer is None else self.get_Q(self.normalizer.normalize(state))
            return int(torch.argmax(q_values))

    def get_Q(self, normalized_states: np.ndarray) -> torch.FloatTensor:
        normalized_states = torch.Tensor(normalized_states.reshape(-1, self.input_dim))
        self.dqn.train(mode=False)
        return self.dqn(normalized_states)
    
    def add_sample(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> None:
        if self.normalizer is None:
            self.memory.push(state, action, reward, next_state, done)
        else:
            normalized_state = self.normalizer.normalize(state)
            normalized_next_state = self.normalizer.normalize(next_state)
            self.memory.push(normalized_state, action, reward, normalized_next_state, done)
        
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
        Q_target = Q_predict.clone().data.numpy()
        """ Q_target is an numpy.ndarray of size (len(minibatch), num_actions).
            At this point Q_target[np.arange(len(Q_target)), actions]) is a 1-dim array of size len(minibatch) and each element is selected from
            the corresponding row. Which cell in the row is used depends on the value of the corresponding actions
            For example, suppose len(minibatch) = 2 and num_actions=3 and Q_target is [[1, 2, 3], [4, 5, 6]] and actions = [1, 0]
            Q_target[np.arange(len(Q_target)), actions]) is then a 1-dim array of size len(minibatch) -> [2, 4], 
            where 2 is taken from the 1st element of [1,2,3] and 4 from the zeroth of [4,5,6].
            However, more importantly here, Q_target[np.arange(len(Q_target)), actions]) represents locations whose values are to be replaced
        """
        Q_target[np.arange(len(Q_target)), actions] = self.get_q_update(rewards, normalized_next_states, done)
        Q_target = torch.Tensor(Q_target)
        """
            Exactly one cell in each row in Q_target has been updated. In other words, the nth row of Q_predict and 
            the nth row of Q_target differs by one value
        """
        return self._train(Q_predict, Q_target)
    
    def get_q_update(self, rewards: np.ndarray, normalized_next_states: np.ndarray, done: np.ndarray):
        return rewards + self.gamma * np.max(self.get_Q(normalized_next_states).data.numpy(), axis=1) * ~done

    def _train(self, Q_pred: torch.FloatTensor, Q_true: torch.FloatTensor) -> float:
        """Computes loss and backpropagation
        Args:
            Q_pred (torch.FloatTensor): Predicted value by the network,
                2-D Tensor of shape(n, output_dim)
            Q_true (torch.FloatTensor): Target value obtained from the game,
                2-D Tensor of shape(n, output_dim)
        Returns:
            float: loss value
        """
        self.dqn.train(mode=True)
        self.optim.zero_grad()
        loss = self.loss_fn(Q_pred, Q_true)
        loss.backward()
        self.optim.step()
        self.loss = loss
        return loss
    
    @override(TorchSeedableAgent)
    def episode_start(self, activity_context: ActivityContext):
        min_eps = 0.01
        slope = (min_eps - 1.0) / (activity_context.num_episodes - 1)
        self.current_epsilon = max(slope * activity_context.episode + 1.0, min_eps)
            
    def get_epsilon(self):
        return self.current_epsilon