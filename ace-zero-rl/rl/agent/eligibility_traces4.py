import rl_utils
__author__ = 'bkurniawan'

from rlagents.rl_agent.eligibility_traces import EligibilityTracesAgent

class EligibilityTracesAgent4(EligibilityTracesAgent):
    """
    This class represents an RL agent that uses replacing traces. Similar to EligibilityTracesAgent2, but with different is_terminal()
    """
    def __init__(self, params_filename=None):
        super(EligibilityTracesAgent4, self).__init__()

    def is_terminal(self, state):
        zone, speed = rl_utils.get_zone_and_speed(state)
        return (zone > 130 or zone==0 or (zone<40 and speed > 2))
        #return zone > 130 or zone==0 or (zone<47 and speed > 2) --> could not catch up, hovering around 95-96
        #return zone > 130 or zone==0 or (zone<43 and speed > 2) --> could not catch up, hovering around 75-78
        #return zone > 130 or zone==0 or (zone<37 and speed > 2) --> could not brake
    