import sys
import os
import random
import time
from pathlib import Path
import ace_zero_core
import rl
from ace_zero_core import acezero
from rl import rl_utils
from rl.context import Context
from rl.listener.total_rewards_listener import TotalRewardsListener
from datetime import datetime
from rl.env.ace_zero_env import AceZeroEnvironment
from array import array
import numpy as np
import argparse
from itertools import count
from collections import namedtuple
from datetime import datetime
import torch

start_time = datetime.now()
start_time_string = start_time.strftime("%d/%m/%Y %H:%M:%S")
print("start date/time =", start_time_string)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

NUM_TICKS = 700
NUM_EPISODES = 20000
scenario_name = 'ac2d5A-007.json'
env = AceZeroEnvironment(scenario_name)
NUM_STATES = 14000
NUM_ACTIONS = len(env.actions)
ALPHA_THETA = 0.5
ALPHA_W = 0.5
GAMMA = 0.95
LAMBDA_THETA = 0.9
LAMBDA_W = 0.8

#theta = [[0.0] * NUM_ACTIONS for i in range(NUM_STATES)] #NUM_STATES x NUM_ACTIONS array
#w = [0.0] * NUM_STATES
#z_theta = [[0.0] * NUM_ACTIONS for i in range(NUM_STATES)]
#z_w = [0.0] * NUM_STATES
theta = torch.zeros(NUM_STATES, NUM_ACTIONS, dtype=torch.double, device=device)
w = torch.zeros(NUM_STATES, dtype=torch.double, device=device)
z_theta = torch.zeros(NUM_STATES, NUM_ACTIONS, dtype=torch.double, device=device)
z_w = torch.zeros(NUM_STATES, dtype=torch.double, device=device)
actions = np.arange(NUM_ACTIONS) # don't convert to torch

def softmax(x): # don't convert to torch
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0) 

def select_action(state):
    theta_nd = (theta[state]).data.cpu().numpy()
    prob = softmax(theta_nd)
    return np.random.choice(actions, p=prob)

def discretise_degrees(degrees):
    if degrees <= 10 and degrees >= -10:
        return 0
    if degrees > 10 and degrees <= 30:
        return 1
    if degrees < -10 and degrees >= -30:
        return 2
    if degrees > 30 and degrees <= 50:
        return 3
    if degrees < -30 and degrees >= -50:
        return 4
    if degrees > 50 and degrees <= 70:
        return 5
    if degrees < -50 and degrees >= -70:
        return 6
    if degrees > 70 and degrees <= 90:
        return 7
    if degrees < -70 and degrees >= -90:
        return 8;
    return 9;

def discretise_delta_v(delta_v):
    if delta_v > 20:
        return 0
    if delta_v > 15:
        return 1
    if delta_v > 10:
        return 2
    if delta_v > 5:
        return 3
    if delta_v > 0:
        return 4
    if delta_v > -5:
        return 5
    if delta_v > -10:
        return 6
    if delta_v > -15:
        return 7
    if delta_v > -20:
        return 8
    return 9
    
def discretise(state):
    distance_btw_arrows, contact_aa, contact_ata, delta_v = state
    R = distance_btw_arrows // 200
    if R > 13:
        R = 13
    aa = discretise_degrees(contact_aa)   # 0..9
    ata = discretise_degrees(contact_ata) # 0..9
    dv = discretise_delta_v(delta_v)      # 0..9
    return int(R * 1000 + dv * 100 + aa * 10 + ata) # 14,000 combinations

def update_weights(rhat, theta, w, z_theta, z_w):
    # decay traces
    z_w *= LAMBDA_W
    z_theta *= LAMBDA_THETA
    # update weights
    w += ALPHA_W * rhat * z_w
    theta += ALPHA_THETA * rhat * z_theta

def main():
    path = 'rl_results/' + scenario_name
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print(path + ' already exists')
        quit()

    file = open(path + '/viper-all-scores.txt','w')
    running_reward = 10

    for i_episode in range(1, NUM_EPISODES + 1):
        print("episode", i_episode, ", start time", start_time_string)
        # reset environment and episode reward
        state = discretise(env.reset())
        ep_reward = 0
        # reset traces
        #for i in range(NUM_STATES):
        #    z_w[i] = 0.0
        #    for j in range(NUM_ACTIONS):
        #        z_theta[i][j] = 0.0
        z_w[:] = 0.0
        z_theta[:] = 0.0

        oldPrediction = 0.0
        for t in range(1, NUM_TICKS + 1):
            action = select_action(state)

            # take the action
            state, reward, done, _ = env.step(action)
            state = discretise(state)

            prediction = w[state]
            rhat = reward + GAMMA * prediction - oldPrediction
            z_theta[state][action] += (1.0 - LAMBDA_THETA) * 0.5
            z_w[state] += (1.0 - LAMBDA_W)
            update_weights(rhat, theta, w, z_theta, z_w)
            oldPrediction = prediction
            ep_reward += reward
            if done:
                break

        # update cumulative reward
        file.write(str(i_episode) + "," + str(ep_reward / NUM_TICKS) + '\n')
        file.flush()
        running_reward = 0.05 * ep_reward + (1 - 0.05) * running_reward

        # log results
        if i_episode % 10 == 0:
            print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}\t\tAvg reward/episode: {:.2f}'.format(
                  i_episode, ep_reward, running_reward, ep_reward / NUM_TICKS))
    file.close()
    #env.show_trajectory_chart()

if __name__ == '__main__':
    print('device:', device)
    main()
    
    
    end_time = datetime.now()
    end_time_string = end_time.strftime("%d/%m/%Y %H:%M:%S")
    print("end time =", end_time_string)
    delta = end_time - start_time
    print('Learning took ' + str(delta.seconds) + ' seconds')