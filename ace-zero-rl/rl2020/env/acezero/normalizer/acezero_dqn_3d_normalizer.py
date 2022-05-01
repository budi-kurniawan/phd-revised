import numpy as np
from rl2020.normalizer.normalizer import Normalizer

class AceZeroDQN3DNormalizer(Normalizer):
    def normalize(self, state):
        return np.array(((state[0] / 4500.0) - 1, state[1] / 180.0, state[2] / 180.0, state[3] / 40.0, state[4] / 5000))