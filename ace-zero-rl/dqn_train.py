import os
import numpy as np
import random
import pickle
from datetime import datetime
from typing import Tuple
import torch
import ace_zero_core
import rl
from ace_zero_core import acezero
from rl import rl_utils
from rl.env.ace_zero_env import AceZeroEnvironment
from cartpole.util.dqn_util import DQN, ReplayMemory, DQNAgent
from rl.reward_manager import RewardManager

NUM_TRIALS = 10
START_TRIAL = 0
NUM_EPISODES = 20_000
MAX_TICKS = 700
min_epsilon = 0.01
batch_size = 64
gamma = 0.99
hidden_dim = 50
mem_size = 1_000_000

def play_episode(env, agent: DQNAgent, eps: float) -> int:
    agent.init()
    s = env.reset(red_initials=get_red_initials(0))
    s = normalise(s)
    done = False
    total_reward = 0

    for tick in range(MAX_TICKS):
        a = agent.select_action(s, eps)
        s2, r, done, _ = env.step(a)
        s2 = normalise(s2)
        if done:
            r = -1
        total_reward += r
        agent.add_sample(s, a, r, s2, done)
        agent.train()
        s = s2
    agent.after_episode()
    return total_reward

def get_env_dim(env) -> Tuple[int, int]:
    input_dim = 4
    output_dim = 5 # NUM_ACTIONS = len(env.actions)
    return input_dim, output_dim

def epsilon_annealing(epsiode: int, max_episode: int, min_eps: float) -> float:
    slope = (min_eps - 1.0) / max_episode
    return max(slope * epsiode + 1.0, min_eps)

def save_model(path, dqn):
    file = open(path,'wb')
    pickle.dump(dqn, file)
    file.close()

def get_red_initials(episode):
    # x should move from 1500 to 0 in 10 steps, y from -300 to 300 in 10 steps, z and psi remain 0 all the time
    init  = (1500, 300, 0, 50)
    r = random.random() - 0.5 # return -0.5..0.5
    x = init[0] + r * 10
    y = init[1] + r * 2
    z = 0.0
    psi = init[3] + r * 2
    return (x, y, z, psi)

def normalise(state):
    return np.array(((state[0] / 4500.0) - 1, state[1] / 180.0, state[2] / 180.0, state[3] / 40.0))

def get_bootstrap_data(trial):
    return None

def write_to_times_file(results_path, msg):
    times_file = open(results_path + '/times.txt', 'a+')
    times_file.write(msg + '\n')
    times_file.close()

def main(env, input_dim, output_dim, results_path):
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    print('start:\n\b', datetime.now().strftime('%d/%m/%y %H:%M:%S'))
    print('Trial,Learning Time 1 (seconds),Learning Time 2 (seconds),Avg Score 1,Avg Score 2')
    print('=================================================================================')
    
    for trial in range(START_TRIAL, NUM_TRIALS):
        random.seed(trial)
        env.seed(trial)
        np.random.seed(trial)
        torch.manual_seed(trial)
        file = open(results_path + '/viper-all-scores-' + str(trial).zfill(2) + '.txt','w')
        start_time = datetime.now()
        
        reward_manager = RewardManager(5, 0.1) # num_rewards = 5, min_reward = 0.1

        memory = ReplayMemory(mem_size)
        agent = DQNAgent(memory, input_dim, output_dim, hidden_dim)
        agent.bootstrap(get_bootstrap_data(trial), trial, results_path) # to be used in child classes
        total = 0
        
        for episode in range(1, NUM_EPISODES + 1):
            eps = epsilon_annealing(episode, NUM_EPISODES - 1, min_epsilon)
            ep_reward = play_episode(env, agent, eps)
            avg_reward = ep_reward / MAX_TICKS
            total += avg_reward
            print("1st [Trial: {:2}], [Episode: {:5}] avg reward: {:5} ".format(trial, episode, avg_reward))
            file.write(str(episode) + "," + str(avg_reward) + '\n')
            
            added, removed = reward_manager.probably_add(avg_reward, episode)
            if added is not None:
                if removed is not None:
                    model_path = results_path + '/model' + str(trial).zfill(2) + '-' + str(removed[1]).zfill(6) + '-' + format(removed[0], '.2f') + '.p'
                    if os.path.exists(model_path):
                        os.remove(model_path)
                save_model(results_path + '/model' + str(trial).zfill(2) + '-' 
                        + str(added[1]).zfill(6) + '-' + format(added[0], '.2f') + '.p', agent.dqn)
            
        print('average reward:', total / NUM_EPISODES)
        end_time = datetime.now()
        delta = end_time - start_time
        print('Trial', trial, ', Pytorch DQN learning 1 took ' + str(delta.total_seconds()) + ' seconds')
        print('trial', trial, ', avg score:', total / (NUM_EPISODES))
        write_to_times_file(results_path, 'Trial ' + str(trial) + ' DQN learning 1 took ' + str(delta.total_seconds()) + ' seconds\n')
        save_model(results_path + '/model' + str(trial).zfill(2) + '-' + str(NUM_EPISODES) + '.p', agent.dqn)
        
        ### 2nd batch
        start_time = datetime.now()
        for episode in range(1 + NUM_EPISODES, NUM_EPISODES * 2 + 1):
            eps = epsilon_annealing(episode, NUM_EPISODES - 1, min_epsilon)
            ep_reward = play_episode(env, agent, eps)
            avg_reward = ep_reward / MAX_TICKS
            total += avg_reward
            print("2nd [Trial: {:2}], [Episode: {:5}] avg reward: {:5} ".format(trial, episode, avg_reward))
            file.write(str(episode) + "," + str(avg_reward) + '\n')

            added, removed = reward_manager.probably_add(avg_reward, episode)
            if added is not None:
                if removed is not None:
                    model_path = results_path + '/model' + str(trial).zfill(2) + '-' + str(removed[1]).zfill(6) + '-' + format(removed[0], '.2f') + '.p'
                    if os.path.exists(model_path):
                        os.remove(model_path)
                save_model(results_path + '/model' + str(trial).zfill(2) + '-' 
                        + str(added[1]).zfill(6) + '-' + format(added[0], '.2f') + '.p', agent.dqn)

        file.close()
        print('average reward:', total / (NUM_EPISODES * 2))
        
        end_time = datetime.now()
        delta = end_time - start_time
        print('Trial', trial, ', Pytorch DQN learning 2 took ' + str(delta.total_seconds()) + ' seconds')
        print('trial', trial, ', avg score:', total /  (NUM_EPISODES * 2))
        write_to_times_file(results_path, 'Trial ' + str(trial) + ' DQN learning 2 took ' + str(delta.total_seconds()) + ' seconds\n\n')
        save_model(results_path + '/model' + str(trial).zfill(2) + '-' + str(2*NUM_EPISODES) + '.p', agent.dqn)

if __name__ == '__main__':
    scenario_name = 'standard-001.json'
    results_name = 'dqn-001.json'
    env = AceZeroEnvironment(scenario_name)
    input_dim, output_dim = get_env_dim(env)
    results_path = 'rl_results/' + results_name
    main(env, input_dim, output_dim, results_path)