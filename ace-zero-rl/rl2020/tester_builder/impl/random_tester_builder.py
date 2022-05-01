from rl2020.tester_builder.tester_builder import TesterBuilder
from rl2020.util.util import override
from rl2020.tester.random_tester import RandomTester

class RandomTesterBuilder(TesterBuilder):

    def __init__(self, num_actions) -> None:
        self.num_actions = num_actions
    
    @override(TesterBuilder)
    def create_tester(self, trial):
        return RandomTester(self.num_actions, trial)