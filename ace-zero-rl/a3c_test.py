#!/usr/bin/env python3
import sys
import os
import random
import time
from pathlib import Path
from datetime import datetime
import torch
import torch.nn
import numpy as np
from collections import namedtuple
from sklearn.neural_network import MLPClassifier
from datetime import datetime
import time
import pickle

import ace_zero_core
import rl
from ace_zero_core import acezero
from rl import rl_utils
from rl.env.ace_zero_env import AceZeroEnvironment
from a3c_train import normalise, Net, v_wrap

input_dim = 4

#def _to_variable(x: np.ndarray) -> torch.Tensor:
#    return torch.autograd.Variable(torch.Tensor(x))

#def get_Q(dqn, states: np.ndarray) -> torch.FloatTensor:
#    states = _to_variable(states.reshape(-1, input_dim))
#    dqn.train(mode=False)
#    return dqn(states)

#def select_test_action(dqn, states):
#    dqn.train(mode=False)
#    scores = get_Q(dqn, states)
#    _, argmax = torch.max(scores.data, 1)
#    return int(argmax.numpy())

def test(model_path, scenario_name, num_ticks):
    env = AceZeroEnvironment(scenario_name)
    lnet = pickle.load(open(model_path, "rb"))
    num_inputs = input_dim
    ep_reward = 0
    state = env.reset()
    state = normalise(state)
    for tick in range(1, num_ticks):
        action = lnet.select_action(v_wrap(state[None, :]))
        state, reward, done, _ = env.step(action)
        state = normalise(state)
        ep_reward += reward
        if done:
            break
    return (0.5 + ep_reward/num_ticks)

if __name__ == '__main__':
    num_ticks = 1000
    NUM_TRIALS = 10
    for trial in range(NUM_TRIALS):
        #model_path = 'rl_results/a3c-001.json-windows-good/model0' + str(trial) + '-20000.p'
        model_path = 'rl_results/a3c-001.json-windows-200k/model0' + str(trial) + '-200000.p'
        rewards = [] #[trial]
        for i in range(1, 5):
            scenario_name = 'd2dspl.mytest00' + str(i) + '.json'
            ep_reward = test(model_path, scenario_name, num_ticks)
            rewards.append(ep_reward)
        print(*rewards, sep=',')