from rl2020.discretizer.discretizer import Discretizer

class GridworldDiscretizer(Discretizer):
    def __init__(self, num_state_vars):
        self.num_states = num_state_vars
        
    def get_num_discrete_states(self):
        return self.num_states
    
    def discretize(self, state):
        return int(state)