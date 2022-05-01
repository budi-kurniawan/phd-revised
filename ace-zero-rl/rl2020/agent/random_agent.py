__author__ = 'bkurniawan'
from rl2020.agent.seedable_agent import SeedableAgent

""" A class representing random agents """
class RandomAgent(SeedableAgent):
    
    def __init__(self, num_actions: int, seed=None):
        super().__init__(seed)
        self.num_actions = num_actions

    def select_action(self, state: int) -> int:
        return self.np_random.choice(self.num_actions)