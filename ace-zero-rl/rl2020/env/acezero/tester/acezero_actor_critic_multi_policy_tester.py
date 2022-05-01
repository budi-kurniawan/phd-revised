import pickle
from rl2020.tester.tester import Tester

class AceZeroActorCriticMultiPolicyTester(Tester):
    def __init__(self, policy_paths, discretizer):
        self.thetas = []
        for policy_path in policy_paths:
            file = open(policy_path, 'rb')
            self.thetas.append(pickle.load(file))
            file.close()
        self.discretizer = discretizer