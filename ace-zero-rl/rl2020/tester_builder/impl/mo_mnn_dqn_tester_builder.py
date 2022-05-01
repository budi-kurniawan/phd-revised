from rl2020.util.util import override
from rl2020.tester_builder.impl.mo_dqn_tester_builder import MultiObjectiveDQNTesterBuilder
from rl2020.tester.mo_mnn_dqn_tester import MultiObjectiveMultiNNDQNTester

class MultiObjectiveMultiNNDQNTesterBuilder(MultiObjectiveDQNTesterBuilder):
    
    @override(MultiObjectiveDQNTesterBuilder)
    def __init__(self, policy_path: str, **kwargs) -> None:
        self.policy_path = policy_path
        self.normalizer = kwargs.get('normalizer', None)
        self.input_dim = kwargs.get('input_dim', None)
        self.original_output_dim = kwargs.get('original_output_dim', None)
        self.num_rewards = kwargs.get('num_rewards', None)

    @override(MultiObjectiveDQNTesterBuilder)
    def create_tester(self, trial):
        return MultiObjectiveMultiNNDQNTester(self.policy_path, normalizer=self.normalizer, input_dim=self.input_dim, 
                original_output_dim=self.original_output_dim, num_rewards=self.num_rewards)
