from rl2020.tester_builder.tester_builder import TesterBuilder
from rl2020.util.util import override
from rl2020.env.acezero.tester_builder.acezero_actor_critic_multi_policy_tester_builder import AceZeroActorCriticMultiPolicyTesterBuilder
from rl2020.env.acezero.tester.acezero_actor_critic_multi_policy_tester_001 import AceZeroActorCriticMultiPolicyTester001

class AceZeroActorCriticMultiPolicyTesterBuilder001(AceZeroActorCriticMultiPolicyTesterBuilder):
    @override(TesterBuilder)
    def create_tester(self, trial):
        return AceZeroActorCriticMultiPolicyTester001(self.policy_paths, discretizer=self.discretizer)