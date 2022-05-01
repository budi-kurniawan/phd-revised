import torch
import torch.nn

from rl2020.tester.dqn_tester import DQNTester
from rl2020.util.util import override

class MultiObjectiveDQNTester(DQNTester):
    @override(DQNTester)
    def __init__(self, policy_path, **kwargs):
        self.original_output_dim = kwargs.get('original_output_dim', None)
        super().__init__(policy_path, **kwargs)
        
    @override(DQNTester)
    def select_action(self, state)->int:
        if self.normalizer is not None:
            state = self.normalizer.normalize(state)
        q_values = self.get_Q(state)
        individual_scores = torch.split(q_values.data[0], self.original_output_dim)
        sum_of_scores = torch.zeros(self.original_output_dim)
        for i in range(len(individual_scores)):
            sum_of_scores += individual_scores[i]
        return int(torch.argmax(sum_of_scores))
    
