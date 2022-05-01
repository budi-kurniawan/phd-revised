__author__ = 'bkurniawan'

from rlagents.rl_agent.eligibility_traces4 import EligibilityTracesAgent4

class EligibilityTracesAgent6(EligibilityTracesAgent4):
    """
    EligibilityTraceAgent with constant epsilon
    """
    def __init__(self, params_filename=None):
        super(EligibilityTracesAgent6, self).__init__()

    def get_effective_epsilon(self, epsilon):
        return epsilon
