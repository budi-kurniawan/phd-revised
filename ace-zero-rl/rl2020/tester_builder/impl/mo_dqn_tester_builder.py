from rl2020.util.util import override
from rl2020.tester.mo_dqn_tester import MultiObjectiveDQNTester
from rl2020.tester_builder.impl.dqn_tester_builder import DQNTesterBuilder

class MultiObjectiveDQNTesterBuilder(DQNTesterBuilder):
    
    @override(DQNTesterBuilder)
    def __init__(self, policy_path: str, **kwargs) -> None:
        self.policy_path = policy_path
        self.normalizer = kwargs.get('normalizer', None)
        self.input_dim = kwargs.get('input_dim', None)
        self.original_output_dim = kwargs.get('original_output_dim', None)

    @override(DQNTesterBuilder)
    def create_tester(self, trial):
        return MultiObjectiveDQNTester(self.policy_path, normalizer=self.normalizer, input_dim=self.input_dim, original_output_dim=self.original_output_dim)
