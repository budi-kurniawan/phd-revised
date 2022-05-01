""" A class representing D2D-SQL agents with fixed epsilon """
from rl2020.util.util import override
from rl2020.activity.activity_context import ActivityContext
from rl2020.agent.dqn_agent import DQNAgent
from rl2020.agent.d2dsql_agent import D2DSQLAgent

__author__ = 'bkurniawan'

class D2DSQLAgent2(D2DSQLAgent):    
    @override(DQNAgent)
    def episode_start(self, activity_context: ActivityContext):
        self.current_epsilon = 0.05