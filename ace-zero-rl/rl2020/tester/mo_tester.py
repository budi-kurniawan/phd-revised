""" A Tester is used to test a policy in MORL """
from rl2020.util.util import override
from rl2020.tester.tester import Tester

__author__ = 'bkurniawan'

class MultiObjectiveTester(Tester):

    @override(Tester)
    def __init__(self, policy_path, **kwargs):
        self.num_rewards = kwargs.get('num_rewards', None)
        self.id = kwargs.get('id', None)
        super().__init__(policy_path, **kwargs)