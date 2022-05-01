__author__ = 'bkurniawan'

from rlagents.rl_agent.base_agent import BaseAgent
import utils as ut
from subprocess import *

class ToyAgent(BaseAgent):
    """
    This class represents an agent that can only do simple things. Used for learning/activity
    """
    
    def tick(self, t, dt):
        BaseAgent.tick(self, t, dt)
        self.commands = []
#         if t < 50:
#             self.decrease_speed()
        if t < 1.1:
#             print "min speed at t " + str(t) + ": ", self.get_my_minimum_speed()
#             print "max speed at t " + str(t) + ": ", self.get_my_maximum_speed()
            print("v at t " + str(t) + ": ", self.get_my_speed(), ", v_c:", self.get_my_commanded_speed())
#             print "commanded speed at t " + str(t) + ": ", self.get_my_commanded_speed()
            self.set_minimum_speed()

    def get_relative_angle(self):
        return self.beliefs.entity_state.psi_c - self.beliefs.threat_state.psi_c


