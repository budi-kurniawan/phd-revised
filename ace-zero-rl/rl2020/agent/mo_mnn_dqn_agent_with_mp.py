""" A class representing DQN agents for MORL and multiple neural networks, one for each reward"""

from rl2020.agent.torch_seedable_agent import TorchSeedableAgent
from rl2020.agent.dqn.dqn import DQN, ReplayMemory
from rl2020.util.util import override
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Dict
from multiprocessing import Queue, Process
from rl2020.activity.activity_context import ActivityContext

__author__ = 'Budi Kurniawan'
""" This one uses multiprocessing, but do not use because it is known to crash right before 100,000 episodes. Use the agent in mo_mnn_dqn_agent.py """
class Worker(Process):
    def __init__(self, worker_id, task_queue, response_queue, dqn_dims, normalizer):
        super().__init__()
        self.worker_id, self.task_queue, self.response_queue = worker_id, task_queue, response_queue
        self.dqn = DQN(dqn_dims)
        self.input_dim = dqn_dims[0]
        self.output_dim = dqn_dims[-1]
        self.loss_fn = nn.MSELoss()
        self.optim = optim.Adam(self.dqn.parameters())
        self.normalizer = normalizer
        self.gamma = 0.99

    @override(Process)
    def run(self):
        while True:
            command, data = self.task_queue.get()
            # command is either 'e' (exit), 'a' (select_action), 't' (train) or 's' (save policy)
            if command == 'e':
                print('break. worker ', self.worker_id)
                break
            elif command == 'a':
                normalized_state = data
                #print('select action of worker', self.worker_id, ', normalized state:', normalized_state)
                Q = self.get_Q(normalized_state)
                #print('select action of worker', self.worker_id, ', Q:', Q)
                self.response_queue.put(Q.data.numpy()[0])
            elif command == 't':
                self.train(data)
                #self.response_queue.put(None)
            elif command == 's':
                self.save_policy(data)
                self.response_queue.put(None)
            
    # copied from DQNAgent and modified
    def get_Q(self, normalized_states: np.ndarray) -> torch.FloatTensor:
        normalized_states = torch.Tensor(normalized_states.reshape(-1, self.input_dim))
        self.dqn.train(mode=False)
        return self.dqn(normalized_states)

    # copied from DQNAgent and modified
    def train(self, minibatch) -> None:
        normalized_states = np.vstack([x.state for x in minibatch])
        actions = np.array([x.action for x in minibatch])
        #rewards = np.array([x.reward for x in minibatch])
        worker_id = self.worker_id
        #rewards = np.array([x.reward for x in minibatch])  # split rewards based on self.id
        #print('worker_id:', worker_id, ' rewards:', rewards, '\n')
        rewards = np.array([x.reward[worker_id] for x in minibatch])  # split rewards based on self.id
        normalized_next_states = np.vstack([x.next_state for x in minibatch])
        done = np.array([x.done for x in minibatch])
        
        Q_predict = self.get_Q(normalized_states)
        Q_target = Q_predict.clone().data.numpy()
        Q_target[np.arange(len(Q_target)), actions] = rewards + self.gamma * np.max(self.get_Q(normalized_next_states).data.numpy(), axis=1) * ~done
        Q_target = torch.Tensor(Q_target)
        """
            Exactly one cell in each row in Q_target has been updated. In other words, the nth row of Q_predict and 
            the nth row of Q_target differs by one value
        """
        return self._train(Q_predict, Q_target)

    # copied from DQNAgent and modified
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
    
    # copied from DQNAgent
    def save_policy(self, path): # used to save a policy that can be used for activity
        path = path + '_' + str(self.worker_id)
        file = open(path, 'wb')
        pickle.dump(self.dqn, file)
        file.close()


class MultiObjectiveMultiNNDQNAgentWithMultiProcessing(TorchSeedableAgent):
    def __init__(self, memory_size, batch_size, dqn_dims, normalizer, reward_builder, seed=None) -> None:
        super().__init__(seed)
        self.input_dim = dqn_dims[0]
        self.output_dim = dqn_dims[-1]
        self.reward_builder = reward_builder
        num_rewards = self.num_rewards = reward_builder.get_num_rewards()
        self.memory = ReplayMemory(memory_size, self.random)
        self.batch_size = batch_size
        self.task_queues = [Queue() for _ in range(num_rewards)]
        self.response_queues = [Queue() for _ in range(num_rewards)]
        self.normalizer = normalizer
        self.gamma = 0.99
        self.workers = [Worker(i, self.task_queues[i], self.response_queues[i], dqn_dims, normalizer) for i in range(num_rewards)]
        [worker.start() for worker in self.workers]

    @override(TorchSeedableAgent)
    def trial_end(self, activity_context: ActivityContext)->None:
        [task_queue.put(('e', None)) for task_queue in self.task_queues]
                
    def update(self, learning_context: ActivityContext, state:np.ndarray, action: int, reward: List[float], next_state:np.ndarray, terminal: bool, env_data: Dict[str, object]) -> None:
        rewards = self.reward_builder.get_rewards(env_data)
        self.total_rewards = np.add(rewards, self.total_rewards)
        self.total_redefined_reward += np.sum(rewards)
        self.add_sample(state, action, rewards, next_state, terminal)

        if len(self.memory) > self.batch_size:
            minibatch = self.memory.pop(self.batch_size)
            [task_queue.put(('t', minibatch)) for task_queue in self.task_queues] # no response expected
        
    def save_policy(self, path): # used to save a policy that can be used for activity
        [task_queue.put(('s', path)) for task_queue in self.task_queues]
        # get() expects None, so don't need to do anything other than wait until all workers are finished
        [response_queue.get() for response_queue in self.response_queues]
        
    def select_action(self, state: np.ndarray) -> int:
        if self.np_random.random() < self.current_epsilon:
            return self.np_random.choice(self.output_dim)
        else:
            #self.dqn.train(mode=False)
            #q_values = self.get_Q(state) if self.normalizer is None else self.get_Q(self.normalizer.normalize(state))
            #return int(torch.argmax(q_values))
            normalized_state = state if self.normalizer is None else self.normalizer.normalize(state)
            [task_queue.put(('a', normalized_state)) for task_queue in self.task_queues]
            responses = [response_queue.get() for response_queue in self.response_queues]
            #print('select action: responses:', responses)
            sum_of_Qs = np.sum(responses, axis=0)
            action = np.argmax(sum_of_Qs)
            #print('sum:', sum_of_Q, ', action:', action)
            return action

    def add_sample(self, state: np.ndarray, action: int, rewards: List[float], next_state: np.ndarray, done: bool) -> None:
        if self.normalizer is None:
            self.memory.push(state, action, rewards, next_state, done)
        else:
            normalized_state = self.normalizer.normalize(state)
            normalized_next_state = self.normalizer.normalize(next_state)
            self.memory.push(normalized_state, action, rewards, normalized_next_state, done)
    
    @override(TorchSeedableAgent)
    def episode_start(self, activity_context: ActivityContext):
        min_eps = 0.01
        slope = (min_eps - 1.0) / (activity_context.num_episodes - 1)
        self.current_epsilon = max(slope * activity_context.episode + 1.0, min_eps)
        self.total_redefined_reward = 0
        self.total_rewards = np.zeros(self.num_rewards)