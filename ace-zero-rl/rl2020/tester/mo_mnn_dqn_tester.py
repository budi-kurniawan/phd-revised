import pickle
import numpy as np
import torch
import torch.nn

from rl2020.util.util import override
from rl2020.tester.mo_dqn_tester import MultiObjectiveDQNTester

class MultiObjectiveMultiNNDQNTester(MultiObjectiveDQNTester):
    @override(MultiObjectiveDQNTester)
    def __init__(self, policy_path, **kwargs):
        self.num_rewards = kwargs.get('num_rewards', None)
        super().__init__(policy_path, **kwargs)
    
    @override(MultiObjectiveDQNTester)
    def select_action(self, state)->int:
        if self.normalizer is not None:
            state = self.normalizer.normalize(state)
        state = self._to_variable(state.reshape(-1, self.input_dim))
        list_of_q_values = []
        for dqn in self.dqns:
            list_of_q_values.append(dqn(state).cpu().detach().numpy())
        sum_of_Qs = np.sum(list_of_q_values, axis=0)
        action = int(np.argmax(sum_of_Qs))
        return action

    @override(MultiObjectiveDQNTester)
    def load_policy(self)->None:
        self.dqns = []
        for i in range(self.num_rewards):
            file = open(self.policy_path + '_' + str(i), 'rb')
            self.dqns.append(pickle.load(file))
            file.close()
        [dqn.train(mode=False) for dqn in self.dqns]