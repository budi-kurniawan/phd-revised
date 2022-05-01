from unittest import TestCaseimport sys
from rl.agent.base_agent import BaseAgentfrom rl.agent.et_2d1 import EligibilityTraces2D1Agent
class RLUtilsTestCase(TestCase):
#     def setUp(self):#         sys.path.insert(0, "../rl-src")
    def test_base_agent(self):        baseAgent = BaseAgent        self.assertNotEqual(baseAgent, None, 'baseAgent None')        print("base1")
    def test_actions_exists(self):        baseAgent = BaseAgent        actions = baseAgent.actions        self.assertNotEqual(actions, None, 'actions None')        print("base2")            def test_get_action_with_max_q_value(self):        agent = EligibilityTraces2D1Agent()        state = '0|0|0'        q = []        action = agent.get_action_with_max_q_value( q, state)                print(action)
