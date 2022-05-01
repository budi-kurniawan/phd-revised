__author__ = 'bkurniawan'

from rlagents.rl_agent.eligibility_traces import EligibilityTracesAgent

class EligibilityTracesAgent2(EligibilityTracesAgent):
    """
    This class represents an RL agent that uses replacing traces
    """
    def __init__(self, params_filename=None):
        super(EligibilityTracesAgent2, self).__init__()

    def is_terminal(self, state):
        index = state.index('-')
        zone = int(state[:index])
        speed = int(state[index+1:])
        return zone > 130 or zone==0 or (zone<47 and speed > 2)
