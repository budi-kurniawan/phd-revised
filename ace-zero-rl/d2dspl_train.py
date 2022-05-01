#!/usr/bin/env python3
import os
import random
from datetime import datetime
import numpy as np
import pickle
from discretised_utils import discretise_state
import ace_zero_core
from ace_zero_core import acezero
import rl
from rl import rl_utils
from rl.env.ace_zero_env import AceZeroEnvironment
from aircombat_classifier import create_classifier
from rl.agent2.actor_critic_agent import ActorCriticAgent

NUM_EPISODES = 20_000
MAX_TICKS = 700
MAX_NUM_SAMPLES_FOR_CLASSIFIER = 2000
#NUM_SAMPLES_FOR_CLASSIFIER = 1000

NUM_STATES = 14_000
NUM_ACTIONS = 5
NUM_INPUTS = 4 # x, x_dot, theta, theta_dot

def get_red_initials(episode):
    # x should move from 1500 to 0 in 10 steps, y from -300 to 300 in 10 steps, z and psi remain 0 all the time
    init  = (1500, 300, 0, 50)
    r = random.random() - 0.5 # return -0.5..0.5
    x = init[0] + r * 10
    y = init[1] + r * 2
    z = 0.0
    psi = init[3] + r * 2
    return (x, y, z, psi)

def save_classifier_data(path, buffer, theta):
    # consolidated_next_state_stats and consolidated_rewards are not used in D2D-SPL, but are useful in other methods such as hybrid D2D-DDQN
    consolidated_state_stats = np.zeros([NUM_STATES, NUM_INPUTS], dtype=np.float64)
    consolidated_state_visits = np.zeros(NUM_STATES, dtype=np.int32)
    consolidated_next_state_stats = np.zeros([NUM_STATES, NUM_INPUTS], dtype=np.float64)
    consolidated_rewards = np.zeros(NUM_STATES, dtype=np.float32)
    for i in range(len(buffer)):
        # buffer contains results for top episodes
        # ep_reward is the average reward for the episode, reward is a list of all rewards in all timesteps, group by discrete states
        ep, ep_reward, state_stats, state_visits, next_state_stats, reward = buffer[i]
        consolidated_state_stats += state_stats
        consolidated_state_visits += state_visits
        consolidated_next_state_stats += next_state_stats
        consolidated_rewards += reward
    file = open(path, 'w')
    row_count = 0
    for i in range(NUM_STATES):
        if consolidated_state_visits[i] != 0:
            consolidated_state_stats[i] /= consolidated_state_visits[i]
            consolidated_next_state_stats[i] /= consolidated_state_visits[i]
            consolidated_rewards[i] /= consolidated_state_visits[i]
            # changed s1 (corrected error)
            #s1 = np.array2string(state_stats[i], separator=',', precision=4)
            s1 = np.array2string(consolidated_state_stats[i], separator=',', precision=4)
            s2 = np.array2string(theta[i], separator=',', precision=4)
            s3 = np.array2string(consolidated_next_state_stats[i], separator=',', precision=4)
            s4 = np.array2string(consolidated_rewards[i], separator=',', precision=4)
            file.write(str(i) + ',' + s1 + ',' + s2 + ',' + s3 + ',' + s4 + '\n')
            row_count += 1
    file.close()
    print('training set created with ' + str(row_count) + ', rows.')
    
def run_episode(episode_no, agent, state, env, state_stats, state_visits, next_state_stats, reward_stats):
    agent.init(episode_no, NUM_EPISODES)
    ep_reward = 0
    for _ in range(MAX_TICKS):
        discrete_state = discretise_state(state)
        action = agent.select_action(discrete_state)
        next_state, reward, terminal, _ = env.step(action)
        if state_stats is not None:
            state_visits[discrete_state] += 1
            state_stats[discrete_state] += state
            next_state_stats[discrete_state] += next_state
            reward_stats[discrete_state] += reward

        next_discrete_state = discretise_state(next_state)
        agent.step(discrete_state, action, next_discrete_state, reward, terminal)
        state = next_state
        ep_reward += reward
        if terminal:
            break
    agent.clean_up(episode_no, NUM_EPISODES)
    return ep_reward

def load_policy(path):
    file = open(path, 'rb')
    policy = pickle.load(file)
    file.close()
    return policy

def get_policy_path(base_path, trial, episode):
    return base_path + '/policy' + str(trial).zfill(2) + '-' + str(episode) + '.p'

def get_buffer_path(base_path, trial):
    return base_path + '/buffer-' + str(trial).zfill(2) + '.p'

def create_agent(num_states, num_actions):
    return ActorCriticAgent(num_states, num_actions)

def run_trial(trial_no, env, out_path, times_file):
    score_file = open(out_path + '/viper-all-scores-' + str(trial_no).zfill(2) + '.txt','w')    
    agent = create_agent(NUM_STATES, NUM_ACTIONS)
    total = 0
    start_time = datetime.now()
    buffer = []
    
    for i_episode in range(1, NUM_EPISODES + 1):
        state = env.reset(red_initials=get_red_initials(i_episode))        
        state_stats = np.zeros([NUM_STATES, NUM_INPUTS], dtype=np.float64)
        state_visits = np.zeros(NUM_STATES, dtype=np.int32)
        next_state_stats = np.zeros([NUM_STATES, NUM_INPUTS], dtype=np.float64)
        reward_stats = np.zeros(NUM_STATES, dtype=np.float32)
        ep_reward = run_episode(i_episode, agent, state, env, state_stats, state_visits, next_state_stats, reward_stats)
        total += ep_reward/MAX_TICKS
        
        buffer.append((i_episode, ep_reward, state_stats, state_visits, next_state_stats, reward_stats))
        print(str(trial_no) + ': ' + str(i_episode) + ", " + str(ep_reward/MAX_TICKS))
        score_file.write(str(i_episode) + "," + str(ep_reward/MAX_TICKS) + '\n')
        if i_episode % 1000 == 0:
            score_file.flush()
    delta = rl_utils.get_time_delta(start_time)
    buffer.sort(key=lambda tup: tup[1], reverse=True) # sorted by ep_reward, biggest on top
    del buffer[MAX_NUM_SAMPLES_FOR_CLASSIFIER : ] # keep the first n samples with the highest ep_rewards
    
    buffer_file = open(get_buffer_path(out_path, trial_no), 'wb')
    pickle.dump(buffer, buffer_file)
    buffer_file.close()
    
    save_classifier_data(out_path + '/trainingset' + str(trial_no).zfill(2) + '.txt', buffer, agent.get_policy())
    del buffer
        
    print('first ' + str(NUM_EPISODES) + ' episodes learning took ' + str(delta.total_seconds()) + ' seconds')
    print('trial', trial_no, ', avg score:', total / NUM_EPISODES)
    times_file.write('first ' + str(NUM_EPISODES) + ' episodes learning took ' + str(delta.total_seconds()) + ' seconds' + '\n')
    times_file.flush()
    
    policy_path = get_policy_path(out_path, trial_no, NUM_EPISODES)
    agent.save_policy(policy_path)
    
    # for 2nd batch of episodes
    start_time = datetime.now()
    for i_episode in range(NUM_EPISODES + 1, NUM_EPISODES * 2 + 1):
        state = env.reset(red_initials=get_red_initials(i_episode))
        ep_reward = run_episode(i_episode, agent, state, env, None, None, None, None)
        total += ep_reward/MAX_TICKS
        print(str(trial_no) + ': ' + str(i_episode) + ", " + str(ep_reward/MAX_TICKS))
        score_file.write(str(i_episode) + "," + str(ep_reward/MAX_TICKS) + '\n')
    score_file.close()
    delta = rl_utils.get_time_delta(start_time)
    print('second ' + str(NUM_EPISODES * 2) + ' episodes learning took ' + str(delta.total_seconds()) + ' seconds')
    times_file.write('second ' + str(NUM_EPISODES * 2) + ' episodes learning took ' + str(delta.total_seconds()) + ' seconds' + '\n')
    times_file.flush()
    print('trial', trial_no, ', avg score:', total / (NUM_EPISODES * 2))
    policy_path = get_policy_path(out_path, trial_no, NUM_EPISODES * 2)
    agent.save_policy(policy_path)
    
def recreate_training_set(trial, buffer_path, policy, out_path):
    file = open(buffer_path, 'rb')
    buffer = pickle.load(file)
    file.close()
    print("recreate training set. buffer len:", len(buffer))
    del buffer[MAX_NUM_SAMPLES_FOR_CLASSIFIER : ]
    print("buffer len after truncate:", len(buffer))
    save_classifier_data(out_path + '/trainingset' + str(trial).zfill(2) + '.txt', buffer, policy)
    
def run(scenario_name, out_path, num_trials, start_trial):
    env = AceZeroEnvironment(scenario_name)    
    rl_utils.create_dir_if_not_exists(out_path)
    
    print('start learning d2dspl:', datetime.now().strftime('%d/%m/%y %H:%M:%S'))
    times_file = open(out_path + '/times.txt', 'a+')
    print('times file opened')
    for trial in range(start_trial, num_trials):
        print('start trial', trial)
        times_file.write('=== trial ' + str(trial) + '===\n')
        random.seed(trial)
        env.seed(trial)
        np.random.seed(trial)
        #torch.manual_seed(trial)
        buffer_path = get_buffer_path(out_path, trial)
        if os.path.exists(buffer_path):
            print('buffer path for trial ', trial, ' exists. Recreate training set')
            policy = load_policy(get_policy_path(out_path, trial, NUM_EPISODES))            
            recreate_training_set(trial, buffer_path, policy, out_path)
        else:
            run_trial(trial, env, out_path, times_file)
        start_time = datetime.now()
        classifier_score = create_classifier(trial, out_path)
        delta = rl_utils.get_time_delta(start_time)
        print('Classifier learning took ' + str(delta.total_seconds()) + ' seconds')
        times_file.write('classifier learning took ' + str(delta.total_seconds()) + ' seconds\n')
        times_file.write('classifier score ' + str(classifier_score) + '\n\n')
    times_file.close()
    
if __name__ == '__main__':
    scenario_name = 'standard-001.json'
    out_path = 'rl_results/d2dspl-006.json'
    num_trials = 1 #10
    start_trial = 0
    run(scenario_name, out_path, num_trials, start_trial)