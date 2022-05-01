import numpy as np
from rl2020.util.util import override
from rl2020.env.acezero.tester.acezero_actor_critic_multi_policy_tester import AceZeroActorCriticMultiPolicyTester

class AceZeroActorCriticMultiPolicyTester002(AceZeroActorCriticMultiPolicyTester):
    @override(AceZeroActorCriticMultiPolicyTester)
    # Use the most confident
    def select_action(self, state)->int:
        discrete_state = self.discretizer.discretize(state);
        softmax_max_values = [max(self.softmax(theta[discrete_state])) for theta in self.thetas]
        index = np.argmax(softmax_max_values) # select the most confident theta based on its softmax_value
        return np.argmax(self.thetas[index][discrete_state])
        
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)