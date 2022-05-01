from rl2020.listener.trial_listener import TrialListener
from rl2020.util.util import override
import random
from numpy.random import Generator, PCG64

class SeedableTrialListener(TrialListener):

    @override(TrialListener)
    def before_trial(self, event):
        seed = event.activity_context.trial
        self.random = random.Random();
        self.random.seed(seed)
        self.np_random = Generator(PCG64(seed))
