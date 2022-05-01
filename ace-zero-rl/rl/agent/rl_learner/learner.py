import math
from random import randint, random
EPSILON = 0.1
ALPHA = 0.7
GAMMA = 1
MIN_IDEAL_DISTANCE = 152
MAX_IDEAL_DISTANCE = 914

class Learner(object):
    def __init__(self):
        self.actions = []
        self.prev_action = None
        self.prev_state = None
        self.testing = False
    
    def set_q(self, q):
        self.q = q

    def learn(self, t, dt, entity_state, threat_state, agent):
        self.entity_state = entity_state
        self.threat_state = threat_state
    
    def test(self, t, dt, entity_state, threat_state, agent):
        self.entity_state = entity_state
        self.threat_state = threat_state
    
    def get_explore_exploit_action(self, state):
        if random() < EPSILON:
            return self.get_random_action()
        else:
            return self.get_action_with_max_q_value(state)

    def get_random_action(self):
        return randint(0, len(self.actions) - 1)    
    
    # dict.get() is very slow, avoid that!
    def get_max_table_value(self, state):
        q = self.q
        max_value = 0
        for i in range(len(self.actions)):
            key = state + "-" + str(i)
            if key in q:
                value = q[key]
                if value > max_value:
                    max_value = value
        return max_value;

    def get_table_value(self, state_action):
        table = self.q
        return table[state_action] if state_action in table else 0
    
    def get_action_with_max_q_value(self, state):
        q = self.q
        max_value = -10000000
        action = None
        for i in range(0, len(self.actions)):
            key = state + "-" + str(i)
            value = None
            if key in q:
                value = q[key]
                if value > max_value:
                    max_value = value
                    action = i
        if action == None:
            action = self.get_random_action()
        return action;
    
        
class SpeedLearner(Learner):
    def __init__(self):
        super(SpeedLearner, self).__init__()
        self.actions = ['', 'increase_speed()', 'set_minimum_speed()']
        
    def learn(self, t, dt, entity_state, threat_state, agent):
        super(SpeedLearner, self).learn(t, dt, entity_state, threat_state, agent)
        dx = threat_state.x - entity_state.x
        dy = threat_state.y - entity_state.y
        r = math.sqrt(dx * dx + dy * dy)
        action = None
        state = self.get_state(r)
        if self.prev_state == None:
            action = self.get_random_action()
            self.prev_state = state
            self.prev_action = action
        else:
            reward = None
            if state == '1a':
                reward = -1000
            if state == '1b':
                reward = -100
            if state == '1c':
                reward = -50
            if state == '1d':
                reward = -10
            if state == '1e':
                reward = -1
            elif state == '2a':
                reward = 5
            elif state == '2b':
                reward = 3
            elif state == '2c':
                reward = 1
            elif state == '3':
                # a constant reward causes slow convergence, so use a function
                reward = (dx+MAX_IDEAL_DISTANCE)/100
            prev_state_action = self.prev_state + "-" + str(self.prev_action)
            old_value = self.get_table_value(prev_state_action)
            max_q = self.get_max_table_value(self.prev_state)
            new_value = (1 - ALPHA) * old_value + \
                ALPHA * (reward + GAMMA * max_q)
            q = self.q
            q[prev_state_action] = new_value
            self.prev_state = state
            action = self.get_explore_exploit_action(state)
            self.prev_action = action
#             if t < 10.0:
#                 agent.log_file.write(str.format("t:{0}, r:{1}, action:{2}, old:{3}, new:{4}\n", 
#                     t, reward, action, old_value, new_value))
#                 agent.log_file.write("rel angle:" + str(agent.get_relative_angle()) + "\n")
#                 agent.log_file.write(str(q) + "\n")
#                 agent.log_file.write("my v:" + str(entity_state.v) + ", enemy v:" + str(threat_state.v) + "\n")
#                 agent.log_file.write("my v_c:" + str(entity_state.v_c) + ", enemy v_c:" + str(threat_state.v_c) + "\n")
        return self.execute_action(action)
        
    def test(self, t, dt, entity_state, threat_state, agent):
        super(SpeedLearner, self).test(t, dt, entity_state, threat_state, agent)
        dx = threat_state.x - entity_state.x
        dy = threat_state.y - entity_state.y
        r = math.sqrt(dx * dx + dy * dy)
        state = self.get_state(r)
        action = self.get_action_with_max_q_value(state)
        my_speed = agent.get_my_speed()
        agent.log_file.write(str.format("t:{0}, r:{1}, state:{2}, action:{3}, speed:{4}\n", t, r, 
                         state, action, my_speed))
        return self.execute_action(action)
            
    def execute_action(self, action):
        entity_state = self.entity_state
        threat_state = self.threat_state
        dx = int(threat_state.x - entity_state.x)
        if action == 0:
            delta = int((-dx - MIN_IDEAL_DISTANCE) / 35)
            return "match_speed(" + str(delta) + ")"
        else:
            return str(self.actions[action])

    def get_state(self, r):
        zone = None
        if r > 0:
            zone = "1a"
        elif r > -50:
            zone = "1b"
        elif r > -75:
            zone = "1c"
        elif r > -100:
            zone = "1d"
        elif r > -120:
            zone = "1e"
        elif r > -MIN_IDEAL_DISTANCE:
            zone = "2a"
        elif r > -(MIN_IDEAL_DISTANCE + 200):
            zone = "2b"
        elif r > -MAX_IDEAL_DISTANCE:
            zone = "2c"
        else:
            zone = "3"
        return zone
        
        

class DirectionLearner(Learner):
    def __init__(self):
        super(DirectionLearner, self).__init__()
        self.actions = ['', 'increase_speed()', 'set_minimum_speed()']
    

class AltitudeLearner(Learner):
    def __init__(self):
        super(AltitudeLearner, self).__init__()
        self.actions = ['', 'increase_speed()', 'set_minimum_speed()']
    pass
