import pickle
from rl2020.tester.tester import Tester
from rl2020.util.util import override

class D2DSPLActorCriticTracesTester(Tester):
    @override(Tester)
    def __init__(self, policy_path, **kwargs):
        self.input_dim = kwargs.get('input_dim', None)
        super().__init__(policy_path, **kwargs)
        
    @override(Tester)
    def select_action(self, state)->int:
        if self.normalizer is not None:
            state = self.normalizer.normalize(state)
        p = self.classifier.predict([state])
        return p[0]

    def load_policy(self):
        file = open(self.policy_path, 'rb')
        self.classifier = pickle.load(file)
        file.close()