""" A class representing D2D-SQL agents """
import numpy as np
import pickle
import os
import torch
from datetime import datetime
from rl2020.util.util import override
from rl2020.activity.activity_context import ActivityContext
from rl2020.agent.dqn_agent import DQNAgent

__author__ = 'bkurniawan'

class D2DSQLAgent(DQNAgent):
    
    def __init__(self, normalized_training_set_path, target_loss, memory_size, batch_size, dqn_dims, normalizer, seed=None):
        super().__init__(memory_size, batch_size, dqn_dims, normalizer, seed)
        self.target_loss = target_loss
        self.normalized_training_set_path = normalized_training_set_path

    @override(DQNAgent)
    def trial_start(self, activity_context: ActivityContext):
        trial = activity_context.trial
        out_path = activity_context.out_path
        normalized_training_data = self.get_normalized_training_data()
        data_len = len(normalized_training_data)
        for experience in normalized_training_data:
            s, a, r, s2, done, _ = experience
            self.add_sample(s, a, r, s2, done)
    
        start_time = datetime.now()
        minibatch = self.memory.memory
        max_accuracy = 0
        min_loss = float('inf')
        stats_path = out_path + '/d2dsql-stats-0' + str(trial) + '.txt'
        stats_file = open(stats_path, 'w')
        for i in range(1, 1_000_000 + 1):
            # next lines are copied from train() of the parent
            states = np.vstack([x.state for x in minibatch])
            actions = np.array([x.action for x in minibatch])
    
            Q_predict = self.get_Q(states)
            Q_target = Q_predict.clone().data.numpy() # Q_target is not a second network, most of its values are the same as the reward at the current timestep
            for j in range(data_len):
                s, a, r, s2, done, action_prefs = normalized_training_data[j]
                Q_target[j] = action_prefs # we use non-normalised action_prefs and see if it works
    
            Q_target = torch.Tensor(Q_target)
            self._train(Q_predict, Q_target)
            
            loss = self.loss.item()
            if loss < min_loss:
                min_loss = loss
            if i % 1000 == 0:
                # measure accuracy
                Q_predict = self.get_Q(states)
                correct_prediction = data_len
                for j in range(data_len):
                    argmax = np.argmax(Q_predict[j].data.numpy())
                    if argmax != actions[j]:
                        correct_prediction -= 1
                accuracy = correct_prediction / data_len
                if accuracy > max_accuracy:
                    max_accuracy = accuracy
                stats_file.write('iteration ' + str(i) + ', accuracy:' + str(accuracy) + ", max accuracy:" + str(max_accuracy) 
                                 + ', loss:' + str(loss) + ', min Loss:' + str(min_loss) + '\n')
                print('iteration ', i, "accuracy:", accuracy, "max:", max_accuracy, ", loss:", loss, ', min Loss:', min_loss)
            if min_loss < self.target_loss:
                print('loss ' + str(min_loss) + '. Break at iteration' + str(i))
                break
        end_time = datetime.now()
        time_delta = (end_time - start_time).total_seconds()
        stats_file.write('\ninitialization took ' + str(time_delta) + ' seconds\n')
        stats_file.write('min loss: ' + str(min_loss) + ', max score: ' + str(max_accuracy))
        stats_file.close()

    def write_to_learning_times_file(self, out_path, message):
        learning_times_file = open(out_path + '/d2dspl-agent-learning-times.txt', 'a+')
        learning_times_file.write(message + '\n')        
        learning_times_file.close()
        
    def get_normalized_training_data(self):
        print('d2dsql agent. start initialization with normalized training set in ' + self.normalized_training_set_path)
        data = []
        file = open(self.normalized_training_set_path, 'r')
        lines = file.readlines()
        
        for line in lines:        
            # format episode name,[state],[actions preferences],[next state],reward. Example: 1,[1,2,3,4],[1,2,3,4,5,],[1,2,3,4],1
            index1 = line.index(',')
            ep = int(line[0 : index1])
            index1 = line.index('[', index1 + 1)
            index2 = line.index(']', index1 + 1)
            state = line[index1+1 : index2]
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
        return data