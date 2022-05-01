from rl2020.tester_builder.tester_builder import TesterBuilder
from rl2020.util.util import override

class MultiObjectiveTesterBuilder(TesterBuilder):
    @override(TesterBuilder)
    def __init__(self, policy_path: int, **kwargs) -> None:
        super().__init__(policy_path, **kwargs)
        self.num_rewards = kwargs.get('num_rewards', None)