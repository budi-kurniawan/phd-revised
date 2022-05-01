import pickle
import numpy as np
import torch
import torch.nn
from rl2020.tester.tester import Tester
from rl2020.util.util import override

class DQNTester(Tester):
    @override(Tester)
    def __init__(self, policy_path, **kwargs):
        self.input_dim = kwargs.get('input_dim', None)
        super().__init__(policy_path, **kwargs)
        
    @override(Tester)
    def select_action(self, state)->int:
        state = self.normalizer.normalize(state)
        scores = self.get_Q(state)
        _, argmax = torch.max(scores.data, 1)
        return int(argmax.numpy())

    def _to_variable(self, x: np.ndarray) -> torch.Tensor:
        return torch.autograd.Variable(torch.Tensor(x))

    def get_Q(self, state: np.ndarray) -> torch.FloatTensor:
        state = self._to_variable(state.reshape(-1, self.input_dim))
        self.dqn.train(mode=False)
        return self.dqn(state)
    
    def load_policy(self):
        file = open(self.policy_path, 'rb')
        self.dqn = pickle.load(file)
        file.close()