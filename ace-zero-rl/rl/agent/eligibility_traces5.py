__author__ = 'bkurniawan'

from rlagents.rl_agent.eligibility_traces import EligibilityTracesAgent

class EligibilityTracesAgent5(EligibilityTracesAgent):
    """
    Extends EligibilityTracesAgent, but without terminal states in the target zones and NON_GOAL_TERMINAL_REWARD = -1000
    """
    NON_GOAL_TERMINAL_REWARD = -1000
    
    def __init__(self, params_filename=None):
        super(EligibilityTracesAgent5, self).__init__()        