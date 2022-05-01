from rlagents.rl_agent.rl_learner.learner import SpeedLearner, AltitudeLearner,\
    DirectionLearner
__author__ = 'bkurniawan'

from rlagents.rl_agent.base_agent import BaseAgent
from random import randint, random
import math

class RLAgent(BaseAgent):
    """
    This class represents an RL agent and we will use q_speed, q_altitude, q_direction
    For q_speed, we aim to get between 500 and 3000 feet (152m - 914) behind the enemy.
    For q_direction, change the yaw angle.
    For q_altitue, change the pitch angle
    """
    def __init__(self, params_filename=None):
        super(RLAgent, self).__init__()
        self.speed_learner = SpeedLearner()
        self.direction_learner = DirectionLearner()
        #self.altitude_learner = AltitudeLearner()
        self.testing = False

    def set_q_cache(self, q_cache):
        self.speed_learner.set_q(q_cache.get("q_speed"))
        self.direction_learner.set_q(q_cache.get("q_direction"))
        #self.altitude_learner.set_q(q_cache.get("q_altitude"))
    
    def tick(self, t, dt):
        self.commands = []
        entity_state = self.beliefs.entity_state
        threat_state = self.beliefs.threat_state
        if self.testing == True:
            exec("self." + self.speed_learner.test(t, dt, entity_state, threat_state, self))
            #exec("self." + self.direction_learner.test(t, dt, entity_state, threat_state, self))
            #exec("self." + self.altitude_learner.test(t, dt, entity_state, threat_state, self))
        else:
            exec("self." + self.speed_learner.learn(t, dt, entity_state, threat_state, self))
            #exec("self." + self.direction_learner.learn(t, dt, entity_state, threat_state, self))
            #exec("self." + self.altitude_learner.learn(t, dt, entity_state, threat_state, self))
