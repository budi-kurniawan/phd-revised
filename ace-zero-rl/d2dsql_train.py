#!/usr/bin/env python3
import os
import csv
import pickle
from datetime import datetime
import numpy as np
import ace_zero_core
import torch
import rl
from ace_zero_core import acezero
from rl import rl_utils
from rl.env.ace_zero_env import AceZeroEnvironment
from cartpole.util.dqn_util import BootstrappableDoubleDQNAgent
from dqn_train import main, get_env_dim, normalise
import dqn_train as base

INITIAL_NN_MIN_LOSS = 0.001

def bootstrap1(self, init_data, trial, out_path):
    print('init min loss:', INITIAL_NN_MIN_LOSS)
    bootstrap_model_path = out_path + '/bootstrap-model-0' + str(trial) + '.p'
    print('bootstrap. trial ', trial, ', bootstrap_model_path:', bootstrap_model_path)
    if os.path.exists(bootstrap_model_path):
        #file = open(bootstrap_model_path, 'rb')
        #model = pickle.load(file)
        #file.close()
        # problem with load_state_dict for different Pytorch versions
        #self.dqn.load_state_dict(model.state_dict()) # copy weights from dqn1 to dqn2
        #self.dqn = model
        self.load_model(bootstrap_model_path)
        print('bootstrapped file found and model loaded')
        return
        # if this class is derived from DoubleDQNAgent, copy weights to dqn1 and dqn2
        #self.dqn1.load_state_dict(model.state_dict()) # copy weights from dqn1 to dqn2
        #self.dqn2.load_state_dict(model.state_dict()) # copy weights from dqn1 to dqn2
        #self.dqn = self.dqn1

    print("==== bootstraping agent with len(init_data):", len(init_data))
    
    init_data_len = len(init_data)
    for i in range(init_data_len):
        # s and s2 in init_data are NOT normalised
        s, a, r, s2, done, _ = init_data[i]
        s = base.normalise(s)
        s2 = base.normalise(s2)
        self.add_sample(s, a, r, s2, done)

    start_time = datetime.now()
    memory = self.memory.memory
    print('memory length:', len(memory))
    max_accuracy = 0
    min_loss = float('inf')
    stats_path = out_path + '/stats-0' + str(trial) + '.txt'
    stats_file = open(stats_path, 'w')
    for i in range(1, 1_000_000 + 1):
        #minibatch = memory #memory[count : count + batch_size]
        minibatch = memory #memory[count : count + size]
        
        # next lines are copied from train() of the parent
        states = np.vstack([x.state for x in minibatch])
        actions = np.array([x.action for x in minibatch])

        Q_predict = self.get_Q(states)
        Q_target = Q_predict.clone().data.numpy() # Q_target is not a second network, most of its values are the same as the reward at the current timestep
        for j in range(init_data_len):
            s_not_normalised, a, r, s2_not_normalised, done, action_prefs = init_data[j]
            Q_target[j] = action_prefs # we use non-normalised action_prefs and see if it works

        Q_target = torch.Tensor(Q_target)
        self._train(Q_predict, Q_target)
        
        loss = self.loss.item()
        if loss < min_loss:
            min_loss = loss
        if i % 1000 == 0:
            # measure accuracy
            Q_predict = self.get_Q(states)
            correct_prediction = init_data_len
            for j in range(init_data_len):
                argmax = np.argmax(Q_predict[j].data.numpy())
                if argmax != actions[j]:
                    correct_prediction -= 1
            accuracy = correct_prediction / init_data_len
            if accuracy > max_accuracy:
                max_accuracy = accuracy
            print('iteration ', i, "accuracy:", accuracy, "max:", max_accuracy, ", loss:", loss, ', min Loss:', min_loss)
            
#         if i == 50000 or i % 100_000 == 0:
#             end_time = datetime.now()
#             delta = end_time - start_time
#             msg = 'iteration' + str(i) + ', min loss:' + str(min_loss) + ', loss:' + str(loss) + ', bootstrap time:' + str(delta.total_seconds()) + ' seconds'
#             stats_file.write(msg + '\n')
#             intermediate_bootstrap_model_path = out_path + '/bootstrap-model-0' + str(trial) + '-' + str(i).zfill(7) + '.pt'
#             self.save_model(intermediate_bootstrap_model_path)
#             print(msg)

        if min_loss < INITIAL_NN_MIN_LOSS:
            print('loss ' + str(min_loss) + '. Break at iteration' + str(i))
            break
    self.save_model(bootstrap_model_path)
    #file = open(bootstrap_model_path,'wb')
    #pickle.dump(self.dqn, file)
    #file.close()
    stats_file.write('min loss: ' + str(min_loss) + ', max score: ' + str(max_accuracy))
    stats_file.close()

def fixed_epsilon(epsiode: int, max_episode: int, min_eps: float) -> float:
    return 0.05

def epsilon_annealing2(epsiode: int, max_episode: int, min_eps: float) -> float:
    min_eps = 0.01
    slope = (min_eps - 1.0) / max_episode
    return max(slope * epsiode + 0.2, min_eps)

def not_normalise(state):
    print('not normalise')
    return state

def get_bootstrap_data(trial):
    bootstrap_file = bootstrap_training_set_path + '/trainingset0' + str(trial) + '.txt'
    print('get bootstrap_data for trial', trial, bootstrap_file)
    data = []
    file = open(bootstrap_file, 'r')
    lines = file.readlines()
    
    for line in lines:        
        # format episode name,[state],[actions preferences],[next state],reward. Example: 1,[1,2,3,4],[1,2,3,4,5,],[1,2,3,4],1
        index1 = line.index(',')
        ep = int(line[0 : index1])
        index1 = line.index('[', index1 + 1)
        index2 = line.index(']', index1 + 1)
        state = line[index1+1 : index2]
        # data from trainingset0x.txt has NOT been normalised, see create_classifier() in aircombat_classifier.py
        state = [float(s) for s in state.split(',')]
        index1 = line.index('[', index1 + 1)
        index2 = line.index(']', index1 + 1)
        action_prefs = line[index1+1 : index2]
        action_prefs = [float(s) for s in action_prefs.split(',')]
        index1 = line.index('[', index1 + 1)
        index2 = line.index(']', index1 + 1)
        next_state = line[index1+1 : index2]
        next_state = [float(s) for s in next_state.split(',')]
        reward = float(line[index2 + 2 : ])
        action = np.argmax(action_prefs)
        data.append((np.array(state), action, reward, np.array(next_state), False, action_prefs))
    # we can sort data on reward and trim rows here
    return data

base.DQNAgent = BootstrappableDoubleDQNAgent
base.get_bootstrap_data = get_bootstrap_data
base.hidden_dim = 300
base.DQNAgent.bootstrap = bootstrap1
#base.epsilon_annealing = epsilon_annealing2
base.epsilon_annealing = fixed_epsilon
#base.normalise = not_normalise

if __name__ == '__main__':
    #os.environ['OMP_NUM_THREADS'] = '1' --> does not work
    #torch.set_num_threads(1) --> does not work
    scenario_name = 'standard-001.json'
    bootstrap_training_set_path = 'rl_results/ql-d2dspl-001.json'
    out_path = 'rl_results/bootstrapped-dqn-002j.json'
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    print('start:', datetime.now().strftime('%d/%m/%y %H:%M:%S'))

    env = AceZeroEnvironment(scenario_name)
    INITIAL_NN_MIN_LOSS = 0.01 #0.001
    input_dim, output_dim = get_env_dim(env)
    base.NUM_EPISODES = 10_000
    base.START_TRIAL = 0
    base.NUM_TRIALS = 1 + base.START_TRIAL
    main(env, input_dim, output_dim, out_path)
    
