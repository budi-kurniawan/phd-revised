__author__ = 'bkurniawan'from rlagents.rl_agent.eligibility_traces7 import EligibilityTracesAgent7
class EligibilityTracesAgent9(EligibilityTracesAgent7):    """
    Extends EligibilityTracesAgent7 that uses a less 'generous' reward function and 
    use 5 actions instead of 2
    """
    def __init__(self, params_filename=None):
        super(EligibilityTracesAgent9, self).__init__()    actions = [ 'no_command()', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(-20)',
               'change_speed_by_percentage(10)', 'change_speed_by_percentage(20)']