import pickle
import numpy as np
from rl2020.tester.tester import Tester
from rl2020.util.util import override

class QLearningTester(Tester):

    @override(Tester)
    def select_action(self, state)->int:
        discrete_state = self.discretizer.discretize(state);
        return np.argmax(self.q[discrete_state])
    
    @override(Tester)
    def load_policy(self): # called by the constructor
        file = open(self.policy_path, 'rb')
        self.q = pickle.load(file)
        file.close()
