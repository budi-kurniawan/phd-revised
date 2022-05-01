from rl2020.tester_builder.tester_builder import TesterBuilder
from rl2020.util.util import override
from rl2020.tester.dqn_tester import DQNTester
from rl2020.normalizer.normalizer import Normalizer

class DQNTesterBuilder(TesterBuilder):
    
    @override(TesterBuilder)
    def __init__(self, policy_parent_path: str, num_learning_episodes: int, normalizer: Normalizer, input_dim: int) -> None:
        self.policy_parent_path = policy_parent_path
        self.num_learning_episodes = num_learning_episodes
        self.normalizer=normalizer
        self.input_dim=input_dim

    @override(TesterBuilder)
    def create_tester(self, trial):
        #format of policy filename: policy[XX]-[NumLearningEpisodes].p', where XX is the trial, e.g. policy00-100000.p
        policy_path = self.policy_parent_path + 'policy' + str(trial).zfill(2) + '-' + str(self.num_learning_episodes) + '.p'
        print('dqn policy path for activity:', policy_path)
        return DQNTester(policy_path, normalizer=self.normalizer, input_dim=self.input_dim)