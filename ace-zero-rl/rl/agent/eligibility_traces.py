__author__ = 'bkurniawan'
from rl.agent.base_agent import BaseAgentfrom rl import rl_utils

class EligibilityTracesAgent(BaseAgent):    """    This class represents an RL agent with eligibility traces (replacing traces)    It uses Watkin's Q(lambda) (Q-learning + eligibility traces)
    https://stackoverflow.com/questions/40862578/how-to-understand-watkinss-q%CE%BB-learning-algorithm-in-suttonbartos-rl-book
    
    Do not use http://www-anw.cs.umass.edu/~barto/courses/cs687/Chapter%207.pdf (wrong)
    We want to get between 500 and 3000 feet. (500feet is about 152m    and 3000 feet is approximately 914 m or 0.49 nautical miles).    """    EPSILON = 0.2    ALPHA = 0.7    GAMMA = 0.95    LAMBDA = 0.9    NON_GOAL_TERMINAL_REWARD = -1
    max_q = 0    min_q = 0        actions = [ 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)']
    def __init__(self, params_filename=None):        super(EligibilityTracesAgent, self).__init__()        self.prev_action = None        self.prev_state = None        self.testing = False
    def get_q(self):
        return rl_utils.context.q        #return self.q_cache.get("q")
    def get_e(self):
        return rl_utils.context.e

    def get_reward(self, state):        if self.is_terminal(state):            return EligibilityTracesAgent.NON_GOAL_TERMINAL_REWARD        index = state.index('-')        zone = state[:index]        i = int(zone)        return 1 if i >=9 and i <= 46 else 0    def increment_eligibility_trace(self, e, prev_state_action):        e[prev_state_action] = 1            def learn(self, t, dt):        action = None        current_state = self.current_state        if self.prev_state == None:            action = self.get_random_action()        else:            reward = self.get_reward(current_state)            #q = self.get_q()            e = self.get_e()            prev_state_action = self.prev_state + "-" + str(self.prev_action)            # increment e(s,a)            self.increment_eligibility_trace(e, prev_state_action)            action, explore = self.get_explore_or_exploit_action(self.get_effective_epsilon(self.EPSILON), current_state)            greedy_action = action if not explore else self.get_action_with_max_value(current_state)
            greedy = action == greedy_action            q1 = self.get_q_value(current_state + "-" + str(greedy_action))            q0 = self.get_q_value(prev_state_action)
            delta = reward + EligibilityTracesAgent.GAMMA * q1 - q0            # the following for loop + if are more efficient than the above            for state_action in e:                # state_action is an existing key in e, no need to call get_table_value                e_value = e[state_action]                q_update = EligibilityTracesAgent.ALPHA * delta * e_value                # q_update is not 0 because there is no more zero e_value                self.update_q_value(state_action, self.get_q_value(state_action) + q_update)                if greedy:                    e[state_action] = self.GAMMA * self.LAMBDA * e_value            if not greedy:                e.clear()        self.prev_state = current_state        self.prev_action = action        self.execute_action(action)
    
    def get_q_value(self, state_action):
        q = self.get_q()
        return q[state_action] if state_action in q else 0
    
    def update_q_value(self, state_action, value):
        q = self.get_q()
        q[state_action] = value
        
    def get_action_with_max_value(self, state):
        q = self.get_q()
        return super().get_action_with_max_q_value(q, state)
    
    def get_explore_or_exploit_action(self, epsilon, state):
        q = self.get_q()
        return self.get_explore_exploit_action(epsilon, q, state)
        def log(self, t, reward, prev_state_action, q, e):        my_state = self.beliefs.entity_state        threat_state = self.beliefs.threat_state        dx = my_state.x - threat_state.x        self.log_file.write(str.format("t:{0}, dx:{1}, r:{2}, p sa:{3}\n", t, dx, reward, prev_state_action))        self.log_file.write("v:" + str(my_state.v) + "/" + str(threat_state.v))        self.log_file.write(",  v_c:" + str(my_state.v_c) + "/" + str(threat_state.v_c) + "\n")        self.log_file.write("q:" + str(q) + "\n")        self.log_file.write("e:" + str(e) + "\n\n")    def local_log(self):        pass   