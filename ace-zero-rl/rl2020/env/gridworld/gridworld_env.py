import numpy as np

class GridworldEnvironment():
    # reward is -1 or 0 (goal achieved)
    START_STATE = 0
    ACTION_UP = 0
    ACTION_DOWN = 1
    ACTION_LEFT = 2
    ACTION_RIGHT = 3
    
    def __init__(self, num_rows=10, num_cols=10):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.actions = (self.ACTION_UP, self.ACTION_DOWN, self.ACTION_LEFT, self.ACTION_RIGHT)
        self.num_states = num_rows * num_cols
        self.max_state = self.num_states - 1
        self.state = self.START_STATE

    def reset(self):
        self.state = self.START_STATE
        return np.array((self.state))

    def step(self, action):
        if action == self.ACTION_UP and self.state <= self.max_state - self.num_cols:
            self.state += self.num_cols
        elif action == self.ACTION_DOWN and self.state >= self.num_cols:
            self.state -= self.num_cols
        elif action == self.ACTION_LEFT and self.state % self.num_cols != 0:
            self.state -= 1
        elif action == self.ACTION_RIGHT and (self.state + 1) % self.num_cols != 0:
            self.state += 1
        #reward = 0 if self.state == self.max_state else -1
        #reward = 1000 if self.state == self.max_state else -1
        reward = 100 if self.state == self.max_state else -1
        done = self.state == self.max_state
        data = {}
        return np.array((self.state)), reward, done, data
    
    def seed(self, seed):
        pass # do nothing for now
