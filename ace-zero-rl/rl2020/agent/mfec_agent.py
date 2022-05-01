import pickle
import numpy as np
#import os.path
from rl2020.activity.activity_context import ActivityContext
# modified from https://github.com/astier/model-free-episodic-control

from rl2020.agent.torch_seedable_agent import TorchSeedableAgent
#from scipy.misc.pilutil import imresize
from rl2020.agent.mfec.qec import QEC

__author__ = 'bkurniawan'

""" A class representing MFEC agents """
class MFECAgent(TorchSeedableAgent):
    #def __init__(self, memory_size, batch_size, dqn_dims, normalizer, num_episodes, seed=None) -> None:
    #    super().__init__(seed)
    def __init__(self, buffer_size, k, discount, num_actions, projector, seed, initial_policy_path) -> None:
        super().__init__(seed)
        #self.size = (height, width)
        self.memory = []
        self.num_actions = num_actions
        self.qec = QEC(num_actions, buffer_size, k)
        self.projector = projector
        #self.rs = np.random.RandomState(seed)
        #self.projection = self.rs.randn(
        #    state_dimension, height * width
        #).astype(np.float32)
        self.discount = discount
        #self.epsilon = epsilon

        #self.state = np.empty(state_dimension, self.projection.dtype)
        self.action = int
        self.time = 0        

    def update(self, activity_context, state, action, reward, next_state, terminal, env_data) -> None:
        # use the projected state stored by select_action to avoid potentially time-consuming projection
        self.memory.append(
            {
                "state": self.projected_state,
                "action": action,
                "reward": reward,
                "time": self.time,
            }
        )
        if terminal:
            value = 0.0
            for _ in range(len(self.memory)):
                experience = self.memory.pop()
                value = value * self.discount + experience["reward"]
                self.qec.update(
                    experience["state"],
                    experience["action"],
                    value,
                    experience["time"],
                )

        
    def save_model(self, path): # used to save a model for intermediate learning
        pass

    def save_policy(self, path): # used to save a policy that can be used for activity
        file = open(path, 'wb')
        pickle.dump(self.dqn, file)
        file.close()
        
    def load_model(self, path):
        pass

    def select_action(self, state: np.ndarray) -> int:
        self.time += 1
        self.projected_state = self.projector.project(state) #np.dot(self.projection, state)
        if self.np_random.random() < self.current_epsilon:
            return self.np_random.choice(self.num_actions)
        else:
            # Preprocess and project observation to state
            #obs_processed = np.mean(observation, axis=2)
            #obs_processed = imresize(obs_processed, size=self.size)
            #self.state = np.dot(self.projection, obs_processed.flatten())
            values = [
                self.qec.estimate(self.projected_state, action)
                for action in range(self.num_actions)
            ]
            best_actions = np.argwhere(values == np.max(values)).flatten()
            self.action = self.np_random.choice(best_actions)
            return self.action

    def episode_start(self, activity_context: ActivityContext):
        min_eps = 0.01
        slope = (min_eps - 1.0) / (activity_context.num_episodes - 1)
        self.current_epsilon = max(slope * activity_context.episode + 1.0, min_eps)
            
    def get_epsilon(self):
        return self.current_epsilon