from rl2020.tester_builder.tester_builder import TesterBuilder
from rl2020.util.util import override
from rl2020.env.acezero.tester.acezero_actor_critic_multi_policy_tester import AceZeroActorCriticMultiPolicyTester

class AceZeroActorCriticMultiPolicyTesterBuilder(TesterBuilder):
    @override(TesterBuilder)
    def __init__(self, policy_paths, discretizer):
        self.policy_paths = policy_paths
        self.discretizer = discretizer
    
    @override(TesterBuilder)
    def create_tester(self):
        return AceZeroActorCriticMultiPolicyTester(self.policy_paths, discretizer=self.discretizer)