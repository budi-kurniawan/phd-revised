__author__ = 'bkurniawan'

from rlagents.rl_agent.reward_shaping import RewardShapingAgent
import rl_utils

class RewardShapingAgent2(RewardShapingAgent):
    """
    This class represents an RL agent that uses a reward shaping function that is based on the relative distance only
    We want to get between 500 and 3000 feet. (500feet is about 152m
    and 3000 feet is approximately 914 m or 0.49 nautical miles).
    """
    use_shaping = True
    
    def __init__(self, params_filename=None):
        super(RewardShapingAgent2, self).__init__()

    # We want to be within -MAX_IDEAL_DISTANCE and -MIN_IDEAL_DISTANCE
    def get_true_reward(self, dx):
        return 1 if dx > rl_utils.MIN_IDEAL_DISTANCE and dx < rl_utils.MAX_IDEAL_DISTANCE else 0

    def get_shaping_reward(self, dx):
        if dx < rl_utils.MIN_IDEAL_DISTANCE:
            return -0.001 * (rl_utils.MIN_IDEAL_DISTANCE - dx)
        elif dx < -rl_utils.MAX_IDEAL_DISTANCE:
            return -0.001 * (dx - rl_utils.MAX_IDEAL_DISTANCE)
        else: # in target distance
            return 1
        
    def get_reward(self, dx):
        if dx > RewardShapingAgent.MAX_ZONE_BEFORE_TERMINAL * 20 or dx < 0:
            return RewardShapingAgent.NON_GOAL_TERMINAL_REWARD
        if RewardShapingAgent2.use_shaping:
            return self.get_true_reward(dx) + self.get_shaping_reward(dx)
        else:
            return self.get_true_reward(dx)
        
    def learn(self, t, dt):
        my_state = self.beliefs.entity_state
        threat_state = self.beliefs.threat_state
        dx = my_state.x - threat_state.x
        action = None
        state = self.get_state(my_state, threat_state)
        if self.prev_state == None:
            action = self.get_random_action()
        else:
            reward = self.get_reward(self.prev_dx)
            q = self.get_q()
            prev_state_action = self.prev_state + "-" + str(self.prev_action)
            old_value = self.get_table_value(q, prev_state_action)
            max_q, max_q_sa = self.get_max_table_value(q, state)
            new_value = (1 - self.ALPHA) * old_value + self.ALPHA * (reward + self.GAMMA * max_q)
            q[prev_state_action] = new_value
            if t < 0.0:
                self.log(my_state, threat_state, t, dx, reward, prev_state_action, old_value, new_value, q, max_q, max_q_sa)

            action = self.get_explore_exploit_action(self.EPSILON, q, state)
        self.prev_state = state
        self.prev_action = action
        self.execute_action(action)
        self.prev_dx = dx

    def is_terminal(self, state):
        index = state.index('-')
        zone = int(state[:index])
        return zone > RewardShapingAgent.MAX_ZONE_BEFORE_TERMINAL or zone==0
