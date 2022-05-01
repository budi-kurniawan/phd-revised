__author__ = 'bkurniawan'
from rlagents.rl_agent.simple import RLSimpleAgent
from rlagents.rl_agent.base_agent import BaseAgent
import rl_utils

class RLSimpleAgent2(RLSimpleAgent):
    NON_GOAL_TERMINAL_REWARD = -1
    MAX_ZONE_BEFORE_TERMINAL = 130
    
    def __init__(self, params_filename=None):
        super(RLSimpleAgent2, self).__init__()

    def get_reward(self, state):
        if self.is_terminal(state):
            return RLSimpleAgent2.NON_GOAL_TERMINAL_REWARD
        return 1 if self.consecutive_in_goal >= rl_utils.MIN_NUM_IN_GOAL else 0

    def learn(self, t, dt):
        my_state = self.beliefs.entity_state
        threat_state = self.beliefs.threat_state
        action = None
        state = self.get_state(my_state, threat_state)
        if self.prev_state == None:
            action = self.get_random_action()
        else:
            reward = self.get_reward(state)
            q = self.get_q()
            prev_state_action = self.prev_state + "-" + str(self.prev_action)
            old_value = self.get_table_value(q, prev_state_action)
            max_q, max_q_sa = self.get_max_table_value(q, state)
            new_value = (1 - self.ALPHA) * old_value + self.ALPHA * (reward + self.GAMMA * max_q)
            q[prev_state_action] = new_value
            dx = my_state.x - threat_state.x
            action = self.get_explore_exploit_action(self.EPSILON, q, state)
        self.prev_state = state
        self.prev_action = action
        self.execute_action(action)

    def is_terminal(self, state):
        return super(RLSimpleAgent, self).is_terminal(state)