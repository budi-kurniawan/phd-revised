import numpy as np
import pickle
from rl2020.activity.activity_context import ActivityContext
from rl2020.agent.seedable_agent import SeedableAgent

__author__ = 'bkurniawan'

""" A class representing actor-critic (with traces) agents """
class ActorCriticTracesAgent(SeedableAgent):
    ALPHA_THETA = 0.5
    ALPHA_W = 0.5
    GAMMA = 0.95
    LAMBDA_THETA = 0.9
    LAMBDA_W = 0.8
    
    def __init__(self, num_actions: int, discretizer, seed=None, initial_policy_path=None):
        super().__init__(seed)
        self.discretizer = discretizer
        num_state_vars = discretizer.get_num_discrete_states()
        self.num_actions = num_actions
        if initial_policy_path is not None:
            self.load_policy(initial_policy_path)
        else:
            self.theta = np.zeros([num_state_vars, num_actions], dtype=np.float64)
            self.w = np.zeros(num_state_vars, dtype=np.float64)
        self.z_theta = np.zeros([num_state_vars, num_actions], dtype=np.float64)
        self.z_w = np.zeros(num_state_vars, dtype=np.float64)
        self.actions = np.arange(num_actions)        

    def episode_start(self, activity_context: ActivityContext) -> None:
        # reset traces
        self.z_theta[:] = 0.0
        self.z_w[:] = 0.0

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0) 

    def select_action(self, state) -> int:
        discrete_state = self.discretizer.discretize(state)
        prob = self.softmax(self.theta[discrete_state])
        return self.np_random.choice(self.actions, p=prob)

    def decay_traces(self, z_theta, z_w):
        z_theta *= ActorCriticTracesAgent.LAMBDA_THETA
        z_w *= ActorCriticTracesAgent.LAMBDA_W

    def update_weights(self, rhat, theta, w, z_theta, z_w):
        w += ActorCriticTracesAgent.ALPHA_W * rhat * z_w
        theta += ActorCriticTracesAgent.ALPHA_THETA * rhat * z_theta

    def update(self, activity_context, state, action, reward, next_state, terminal, env_data) -> None:
        discrete_state = self.discretizer.discretize(state)
        old_prediction = self.w[discrete_state]
        prediction = 0.0 if terminal else self.w[self.discretizer.discretize(next_state)]
        delta = reward + ActorCriticTracesAgent.GAMMA * prediction - old_prediction
        if not terminal:
            self.z_theta[discrete_state][action] += 0.05 # strengthen the trace for the current state
            self.z_w[discrete_state] += 0.2 # strengthen the trace for the current state
            self.decay_traces(self.z_theta, self.z_w)
        self.update_weights(delta, self.theta, self.w, self.z_theta, self.z_w)

    def save_policy(self, path) -> None:
        file = open(path, 'wb')
        pickle.dump(self.theta, file)
        pickle.dump(self.w, file)
        file.close()
        
    def load_policy(self, path) -> None:
        file = open(path,'rb')
        self.theta = pickle.load(file)
        self.w = pickle.load(file)
        file.close()