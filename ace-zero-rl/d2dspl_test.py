#!/usr/bin/env python3
import sys
import os
import random
#import pickle
import time
from pathlib import Path
#import pandas as pd
import ace_zero_core
import rl
from ace_zero_core import acezero
from rl import rl_utils
from rl.context import Context
from rl.listener.total_rewards_listener import TotalRewardsListener
from datetime import datetime
from rl.env.ace_zero_env import AceZeroEnvironment

import numpy as np
from itertools import count
from collections import namedtuple
from sklearn.neural_network import MLPClassifier
from datetime import datetime
import time
import pickle

def select_action(classifier, state):
    new_state = np.copy(state)
    new_state[0] = new_state[0] / 4500.0
    new_state[1] = new_state[1] / 180.0
    new_state[2] = new_state[2] / 180.0
    new_state[3] = new_state[3] / 40.0
    p = classifier.predict([new_state])
    #print('prediction', p[0])
    return p[0]

def test(model_path, scenario_name, num_ticks):
    classifier = pickle.load(open(model_path, "rb"))
    env = AceZeroEnvironment(scenario_name)
    #file = open(path + '/test-results.txt','w')
    state = env.reset()
    ep_reward = 0
    for t in range(1, num_ticks + 1):
        action = select_action(classifier, state)
        state, reward, done, _ = env.step(action)
        ep_reward += reward
    #env.show_trajectory_chart()
    return (.5 + ep_reward/num_ticks)
    #file.close()

if __name__ == '__main__':
    num_ticks = 1000    
    NUM_TRIALS = 2
    for trial in range(NUM_TRIALS):
        model_path = 'rl_results/ql-d2dspl-001.json/aircombat-classifier0' + str(trial) + '.p'
        rewards = [] #[trial]
        for i in range(1, 5):
            scenario_name = 'd2dspl.mytest00' + str(i) + '.json'
            ep_reward = test(model_path, scenario_name, num_ticks)
            rewards.append(ep_reward)
        print(*rewards, sep=',')
        