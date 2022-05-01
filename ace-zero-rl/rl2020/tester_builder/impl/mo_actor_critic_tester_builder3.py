from rl2020.util.util import override
from rl2020.tester_builder.mo_tester_builder import MultiObjectiveTesterBuilder
from rl2020.tester.mo_actor_critic_tester3 import MultiObjectiveActorCriticTester3

class MultiObjectiveActorCriticTesterBuilder3(MultiObjectiveTesterBuilder):
    @override(MultiObjectiveTesterBuilder)
    def create_tester(self, trial):
        return MultiObjectiveActorCriticTester3(self.policy_path, discretizer=self.discretizer, num_rewards=self.num_rewards)