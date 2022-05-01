__author__ = 'bkurniawan'

from rlagents.rl_agent.eligibility_traces_cql3 import EligibilityTracesCQL3Agent
from rlagents.rl_agent.eligibility_traces import EligibilityTracesAgent
import rl_utils

class EligibilityTracesCQL4Agent(EligibilityTracesCQL3Agent):
    ### A modified coarse Q-learning agent
    def __init__(self, params_filename=None):
        super(EligibilityTracesCQL4Agent, self).__init__()

    def get_reward(self, state):
        if self.is_terminal(state):
            return EligibilityTracesAgent.NON_GOAL_TERMINAL_REWARD
        return 1 if self.consecutive_in_goal >= rl_utils.MIN_NUM_IN_GOAL else 0
