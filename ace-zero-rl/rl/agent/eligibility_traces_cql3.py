__author__ = 'bkurniawan'from rlagents.rl_agent.eligibility_traces_cql1 import EligibilityTracesCQL1Agent
from rlagents.rl_agent.eligibility_traces import EligibilityTracesAgent
class EligibilityTracesCQL3Agent(EligibilityTracesCQL1Agent):
    ### A modified coarse Q-learning agent
    def __init__(self, params_filename=None):
        super(EligibilityTracesCQL3Agent, self).__init__()
    actions = ['change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']    def calculate_t(self, reward):        self.t += reward * EligibilityTracesAgent.GAMMA * EligibilityTracesAgent.LAMBDA