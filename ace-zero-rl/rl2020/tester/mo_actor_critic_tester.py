import pickle
import numpy as np
from rl2020.util.util import override
from rl2020.tester.tester import Tester
from rl2020.tester.mo_tester import MultiObjectiveTester

class MultiObjectiveActorCriticTester(MultiObjectiveTester):
    
    @override(Tester)
    def select_action(self, state)->int:
        discrete_state = self.discretizer.discretize(state)
        q_values_list = [q[discrete_state] for q in self.thetas] # list of x ndarrays where x = num_rewards
        sum_of_q_values = np.sum(q_values_list, axis=0)
        action = np.argmax(sum_of_q_values)
        return action
    
    @override(Tester)
    def load_policy(self):
        self.thetas = []
        for i in range(self.num_rewards):
            path_i = self.policy_path + '_' + str(i)
            file = open(path_i, 'rb')
            self.thetas.append(pickle.load(file))
            file.close()