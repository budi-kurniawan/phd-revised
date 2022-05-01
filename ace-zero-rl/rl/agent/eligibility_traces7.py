__author__ = 'bkurniawan'
from rl.agent.eligibility_traces import EligibilityTracesAgent
import rl_utils

class EligibilityTracesAgent7(EligibilityTracesAgent):
    """
    Extends EligibilityTracesAgent and uses a less 'generous' reward function
    """
    
    def __init__(self, params_filename=None):
        super(EligibilityTracesAgent7, self).__init__()

    def get_reward(self, state):
        if self.is_terminal(state):
            return EligibilityTracesAgent.NON_GOAL_TERMINAL_REWARD
        return 1 if self.consecutive_in_goal >= rl_utils.MIN_NUM_IN_GOAL else 0
