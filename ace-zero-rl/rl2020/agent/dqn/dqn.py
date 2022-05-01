from typing import List
from collections import namedtuple
import numpy as np
import torch
import torch.nn as nn
import random # needed in ReplayMemory

Transition = namedtuple("Transition", ["state", "action", "reward", "next_state", "done"])

class DQN(nn.Module):
    def __init__(self, dims) -> None:
        super().__init__()
        assert  len(dims) == 3
        input_dim = dims[0]
        hidden_dim = dims[1]
        output_dim = dims[2]
        self.layer1 = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.PReLU()
        ) 
        self.layer2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.PReLU()
        )
        self.layer3 = nn.Linear(hidden_dim, output_dim)
 
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

class ReplayMemory(object):
    def __init__(self, size: int, random=None) -> None:
        self.size = size
        self.pointer = 0
        self.memory = []
        self.random = random.Random() if random is None else random

    def push(self, state: np.ndarray, action: int, reward: int, next_state: np.ndarray, done: bool) -> None:
        if len(self) < self.size:
            self.memory.append(Transition(state, action, reward, next_state, done))
        else:
            self.memory[self.pointer] = Transition(state, action, reward, next_state, done)
        self.pointer = (self.pointer + 1) % self.size

    def pop(self, batch_size: int) -> List[Transition]:
        return self.random.sample(self.memory, batch_size)

    def __len__(self) -> int:
        return len(self.memory)