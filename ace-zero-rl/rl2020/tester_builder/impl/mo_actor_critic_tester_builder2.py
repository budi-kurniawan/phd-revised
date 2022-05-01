from rl2020.util.util import override
from rl2020.tester_builder.mo_tester_builder import MultiObjectiveTesterBuilder
from rl2020.tester.mo_actor_critic_tester2 import MultiObjectiveActorCriticTester2

class MultiObjectiveActorCriticTesterBuilder2(MultiObjectiveTesterBuilder):
    @override(MultiObjectiveTesterBuilder)
    def create_tester(self, trial):
        return MultiObjectiveActorCriticTester2(self.policy_path, discretizer=self.discretizer, num_rewards=self.num_rewards)