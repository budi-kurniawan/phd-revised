__author__ = 'bkurniawan'

from rlagents.rl_agent.base_agent import BaseAgent

class RLSimpleAgent(BaseAgent):
    """
    This class represents an RL agent.
    We want to get between 500 and 3000 feet. (500feet is about 152m
    and 3000 feet is approximately 914 m or 0.49 nautical miles).
    """
    EPSILON = 0.3
    ALPHA = 0.7
    GAMMA = 0.95
    NON_GOAL_TERMINAL_REWARD = -1000
    MAX_ZONE_BEFORE_TERMINAL = 120
    actions = [ 'change_speed_by_percentage(10)', 'change_speed_by_percentage(10)']
    
    def __init__(self, params_filename=None):
        super(RLSimpleAgent, self).__init__()
        self.prev_action = None
        self.prev_state = None
        self.testing = False

    def get_q(self):
        return self.q_cache.get("q")
    
    def tick(self, t, dt):
        self.commands = []
        if self.testing == True:
            self.test(t, dt)
        else:
            self.learn(t, dt)
        
    def get_reward(self, prev_state, prev_action, state):
        if self.is_terminal(state):
            return RLSimpleAgent.NON_GOAL_TERMINAL_REWARD
        index = state.index('-')
        zone = state[:index]
        i = int(zone)
        return 1 if i <= 46 and i >= 9 else 0 

    def learn(self, t, dt):
        my_state = self.beliefs.entity_state
        threat_state = self.beliefs.threat_state
        action = None
        state = self.get_state(my_state, threat_state)
        if self.prev_state == None:
            action = self.get_random_action()
        else:
            reward = self.get_reward(self.prev_state, self.prev_action, state)
            q = self.get_q()
            prev_state_action = self.prev_state + "-" + str(self.prev_action)
            old_value = self.get_table_value(q, prev_state_action)
            max_q, max_q_sa = self.get_max_table_value(q, state)
            new_value = (1 - self.ALPHA) * old_value + self.ALPHA * (reward + self.GAMMA * max_q)
            q[prev_state_action] = new_value
            dx = my_state.x - threat_state.x
#             if t < 10.0:
#                 self.log(my_state, threat_state, t, dx, reward, prev_state_action, old_value, new_value, q, max_q, max_q_sa)
            action = self.get_explore_exploit_action(self.EPSILON, q, state)
        self.prev_state = state
        self.prev_action = action
        self.execute_action(action)
    
    def log(self, my_state, threat_state, t, dx, reward, prev_state_action, old_value, new_value, q, max_q, max_q_sa):
        self.log_file.write(str.format("t:{0}, dx:{1}, r:{2}, p sa:{3}, old q:{4}, new q:{5}",
            t, dx, reward, prev_state_action, old_value, new_value))
        #self.log_file.write("rel angle:" + str(self.get_relative_angle()) + "\n")
        self.log_file.write(str.format(", max_q:{0}, max_q_sa:{1}\n", max_q, max_q_sa,))
        #self.log_file.write(str(q) + "\n")
        self.log_file.write("v:" + str(my_state.v) + "/" + str(threat_state.v))
        self.log_file.write(",  v_c:" + str(my_state.v_c) + "/" + str(threat_state.v_c) + "\n")

    def test(self, t, dt):
        my_state = self.beliefs.entity_state
        threat_state = self.beliefs.threat_state
        dx = int(threat_state.x - my_state.x)
        state = self.get_state(my_state, threat_state)
        q = self.get_q()
        action = self.get_action_with_max_q_value(q, state)
        my_speed = self.get_my_speed()
        self.log_file.write(str.format("t:{0}, dx:{1}, state:{2}, action:{3}, speed:{4}\n", t, dx, 
                         state, action, my_speed))
        self.prev_state = state
        self.prev_action = action
        self.execute_action(action)
            
    def execute_action(self, action):
        exec('self.' + self.actions[action])

    def is_terminal(self, state):
        index = state.index('-')
        zone = state[:index]
        speed = state[index+1:]
        i = int(zone)
        return i > RLSimpleAgent.MAX_ZONE_BEFORE_TERMINAL or i==0 or (i<47 and speed > 2) or (i<80 and speed>3)
        