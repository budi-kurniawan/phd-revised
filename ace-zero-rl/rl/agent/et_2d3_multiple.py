import rl_util__author__ = 'bkurniawan'import mathfrom .. import rl_utilsfrom rl.agent.et_2d3 import EligibilityTraces2D3Agentfrom random import random, randint
class EligibilityTraces2D3MultipleAgent(EligibilityTraces2D3Agent):    ### An agent implementing eligibility traces and Q-learning    def __init__(self, params_filename=None):        super(EligibilityTraces2D3MultipleAgent, self).__init__()    def split_state_action(self, state_action):
        index = state_action.rfind('-')        state = state_action[:index]        action = int(state_action[index+1:])        return state, action    def get_q_value(self, state_action):#         q = self.get_q()#         return q[state_action] if state_action in q else 0        state, action = self.split_state_action(state_action)        return rl_utils.get_q_value_from_db(rl_utils.context.cursor, state, action)        def update_q_value(self, state_action, value):        state, action = self.split_state_action(state_action)        context = rl_utils.context        rl_utils.update_q_value_in_db(context.connection, context.cursor, state, action, context.agent_id, value)#         q = self.get_q()#         q[state_action] = value            def get_action_with_max_value(self, state):#         q = self.get_q()#         action = self.get_action_with_max_q_value(q, state)        return rl_utils.get_action_with_max_value_in_db(rl_utils.context.cursor, state)                def get_explore_or_exploit_action(self, epsilon, state):        if random() < epsilon:            return self.get_random_action(), True        else:            return self.get_action_with_max_value(state), False