import pickle
import numpy as np
from rl2020.test.tester import Tester
from rl2020.util.util import override
from rl2020.env.acezero.discretizer.acezero_discretizer_14000 import AceZeroDiscretizer14000

class ActorCriticMultiPolicyTester(Tester):
    def __init__(self, policy_paths, discretizer):
        self.thetas = []
        for policy_path in policy_paths:
            file = open(policy_path, 'rb')
            self.thetas.append(pickle.load(file))
            file.close()
        self.discretizer = discretizer
        
    @override(Tester)
    def select_action(self, state)->int:
        discrete_state = self.discretizer.discretize(state);
        all_q_values = [theta[discrete_state] for theta in self.thetas]
        sum_of_all_q_values = [sum(x) for x in zip(*all_q_values)]
        return np.argmax(sum_of_all_q_values)

if __name__ == '__main__':
    p = '../../rl2020_results/ac-001'
    policy_paths = [p + '/policy00-10000.p', p + '/policy00-20000.p', p + '/policy00-10000.p', p + '/policy00-20000.p']
    discretizer = AceZeroDiscretizer14000()
    tester = ActorCriticMultiPolicyTester(policy_paths, discretizer)
    state = (1500, 0, 10, 0)
    action = tester.select_action(state)
    print(action)