import numpy as np
from rl2020.util.util import override
from rl2020.tester.tester import Tester
from rl2020.tester.mo_actor_critic_tester import MultiObjectiveActorCriticTester

class MultiObjectiveActorCriticTester3(MultiObjectiveActorCriticTester):    
    @override(Tester)
    def select_action(self, state)->int:
        discrete_state = self.discretizer.discretize(state)
        q_values_list = [q[discrete_state] for q in self.thetas] # list of x ndarrays where x = num_rewards
        sum_of_q_values = 0.25 * q_values_list[0] + 0.75 * q_values_list[1]
        return np.argmax(sum_of_q_values)

