import numpy as np
from rl2020.util.util import override
from rl2020.env.acezero.tester.acezero_actor_critic_multi_policy_tester import AceZeroActorCriticMultiPolicyTester

class AceZeroActorCriticMultiPolicyTester001(AceZeroActorCriticMultiPolicyTester):
    @override(AceZeroActorCriticMultiPolicyTester)
    def select_action(self, state)->int:
        index = 0
        discrete_state = self.discretizer.discretize(state);
        range, aa, ata, delta_v = state
        abs_aa = abs(aa)
        abs_ata = abs(ata)
        if abs_ata <= 45 and abs_aa >= 135:
            index = 4
        elif abs_ata >= 45 and abs_ata <= 135:
            if abs_aa >= 135:
                index = 3
            elif abs_aa <= 45:
                index = 2
        elif abs_ata >= 135 and abs_aa > 135:
            index = 1
        theta = self.thetas[index]
        return np.argmax(theta[discrete_state])
