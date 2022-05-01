from rl2020.tester_builder.tester_builder import TesterBuilder
from rl2020.util.util import override
from rl2020.tester.d2dspl_actor_critic_traces_tester import D2DSPLActorCriticTracesTester
from rl2020.normalizer.normalizer import Normalizer

class D2DSPLActorCriticTracesTesterBuilder(TesterBuilder):
    
    @override(TesterBuilder)
    def __init__(self, policy_parent_path: str, num_learning_episodes: int, normalizer: Normalizer) -> None:
        self.policy_parent_path = policy_parent_path
        self.num_learning_episodes = num_learning_episodes
        self.normalizer=normalizer

    @override(TesterBuilder)
    def create_tester(self, trial):
        #format of policy filename: policy[XX]-[NumLearningEpisodes].p', where XX is the trial, e.g. policy00-100000.p
        policy_path = self.policy_parent_path + 'd2dspl-classifier-' + str(trial).zfill(2) + '-' + str(self.num_learning_episodes).zfill(8) + '.p'
        return D2DSPLActorCriticTracesTester(policy_path, normalizer=self.normalizer)