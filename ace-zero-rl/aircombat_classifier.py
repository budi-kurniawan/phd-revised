#!/usr/bin/env python3
import numpy as np
from sklearn.neural_network import MLPClassifier
import pickle

# scikit MLP: https://scikit-learn.org/stable/modules/neural_networks_supervised.html

max_records = 14_000
hidden_layer_sizes = [300, 300]
solver = 'lbfgs'
alpha = 0.0001

def prepare_data(file, max_records=1_000_000):
    X = []
    Y = []
    f = open(file, "r")
    for line in f:
        index1 = line.index('[')
        index2 = line.index(']', index1 + 1)
        x = line[index1 + 1 : index2]
        x = list(x.split(','))
        x = [float(i) for i in x]
        index1 = line.index('[', index2 + 1)
        index2 = line.index(']', index1 + 1)
        y = line[index1 + 1 : index2]
        y = list(y.split(','))
        y = [float(i) for i in y]
        if sum(y) == 0:
            continue
        X.append(x)
        Y.append(np.argmax(y))
        if len(X) == max_records:
            break
    return X, Y

def create_classifier(trial_no, out_path):
    file = out_path + '/trainingset' + str(trial_no).zfill(2) + '.txt'
    pickled_path = out_path + '/aircombat-classifier' + str(trial_no).zfill(2) + '.p'
    X, Y = prepare_data(file, max_records)
    print('len:', len(X), len(Y))
    print(X)
    print('=================\n', Y)
    for i in range(len(X)):
        X[i][0] /= 4500.0
        X[i][1] /= 180.0
        X[i][2] /= 180.0
        X[i][3] /= 40.0
    #classifier = MLPClassifier(solver=solver, alpha=alpha, random_state=1, max_iter=1_000_000, hidden_layer_sizes=hidden_layer_sizes).fit(X, Y)
    #pickle.dump(classifier, open(pickled_path, "wb"))
    #score = classifier.score(X, Y)
    #print('classifier score for trial ' + str(trial_no) + ': ' + str(score))
    #return score

def main():
    num_trials = 1
    out_path = 'rl_results/d2dspl-001.json'
    for trial in range(num_trials):
        np.random.seed(trial)
        create_classifier(trial, out_path)

if __name__ == '__main__':
    main()