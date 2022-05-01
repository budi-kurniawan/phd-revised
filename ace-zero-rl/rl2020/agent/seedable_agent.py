import random
from numpy.random import Generator, PCG64
from rl2020.agent.agent import Agent

class SeedableAgent(Agent):
    def __init__(self, seed):
        self.random = random.Random();
        if seed is None:
            self.np_random = Generator(PCG64())
        else:
            self.random.seed(seed)
            self.np_random = Generator(PCG64(seed))

    def seed(self, seed) -> None:
        self.random.seed(seed)
        self.np_random = Generator(PCG64(seed)) # replace generator bec. once created we cannot change the seed