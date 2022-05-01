#!/usr/bin/env python3
"""
Reinforcement Learning (A3C) using Pytroch + multiprocessing.
The most simple implementation for continuous action.
View more on my Chinese tutorial page (https://morvanzhou.github.io/).

See also https://github.com/ikostrikov/pytorch-a3c
"""
import os
from datetime import datetime
import random
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.multiprocessing as mp
import ace_zero_core
import rl
from ace_zero_core import acezero
from rl import rl_utils
from rl.env.ace_zero_env import AceZeroEnvironment

NUM_EPISODES = 200_000
MAX_TICKS = 700
scenario_name = 'a3c-001.json'
UPDATE_GLOBAL_ITER = 100 #10
GAMMA = 0.9
num_workers = min(4, mp.cpu_count())

num_state_variables = 4
num_actions = 5
hidden_layer_sizes = [100, 50]

def normalise(state):
    return np.array(((state[0] / 4500.0) - 1, state[1] / 180.0, state[2] / 180.0, state[3] / 40.0))

def get_red_initials(episode):
    # x should move from 1500 to 0 in 10 steps, y from -300 to 300 in 10 steps, z and psi remain 0 all the time
    init  = (1500, 300, 0, 50)
    r = random.random() - 0.5 # return -0.5..0.5
    x = init[0] + r * 10
    y = init[1] + r * 2
    z = 0.0
    psi = init[3] + r * 2
    return (x, y, z, psi)

class Net(nn.Module):
    def __init__(self, num_state_variables, num_actions):
        super(Net, self).__init__()
        self.pi1 = nn.Linear(num_state_variables, hidden_layer_sizes[0])
        self.pi2 = nn.Linear(hidden_layer_sizes[0], num_actions)
        self.v1 = nn.Linear(num_state_variables, hidden_layer_sizes[1])
        self.v2 = nn.Linear(hidden_layer_sizes[1], 1)
        set_init([self.pi1, self.pi2, self.v1, self.v2])
        self.distribution = torch.distributions.Categorical

    def forward(self, x):
        pi1 = F.relu6(self.pi1(x))
        logits = self.pi2(pi1)
        v1 = F.relu6(self.v1(x))
        values = self.v2(v1)
        return logits, values

    def select_action(self, state):
        self.eval()
        logits, _ = self.forward(state)
        prob = F.softmax(logits, dim=1).data
        m = self.distribution(prob)
        return m.sample().numpy()[0]

    def loss_func(self, s, a, v_t):
        self.train()
        logits, values = self.forward(s)
        td = v_t - values
        c_loss = td.pow(2)
        
        probs = F.softmax(logits, dim=1)
        m = self.distribution(probs)
        exp_v = m.log_prob(a) * td.detach().squeeze()
        a_loss = -exp_v
        total_loss = (c_loss + a_loss).mean()
        return total_loss

class Worker(mp.Process):
    def __init__(self, trial, gnet, opt, global_ep, global_ep_r, res_queue, name):
        super(Worker, self).__init__()
        self.name = 'w%i' % name
        self.g_ep, self.g_ep_r, self.res_queue = global_ep, global_ep_r, res_queue
        self.gnet, self.opt = gnet, opt
        self.lnet = Net(num_state_variables, num_actions) # local network
        self.env = AceZeroEnvironment(scenario_name)
        self.env.seed(trial)
        self.trial = trial

    def run(self):
        total_step = 1
        while self.g_ep.value <= NUM_EPISODES:
            state = self.env.reset(red_initials=get_red_initials(0))
            state = normalise(state)
            buffer_s, buffer_a, buffer_r = [], [], []
            ep_r = 0
            
            for tick in range(MAX_TICKS):
                a = self.lnet.select_action(v_wrap(state[None, :]))
                next_state, r, done, _ = self.env.step(a)
                next_state = normalise(next_state)
                #if done: r = -1
                ep_r += r
                buffer_a.append(a)
                buffer_s.append(state)
                buffer_r.append(r)

                done = tick == MAX_TICKS - 1
                if done or total_step % UPDATE_GLOBAL_ITER == 0:  # update global and assign to local net
                    # sync
                    push_and_pull(self.opt, self.lnet, self.gnet, done, next_state, buffer_s, buffer_a, buffer_r, GAMMA)
                    buffer_s, buffer_a, buffer_r = [], [], []

                    if done:  # done and print information
                        record(self.trial, self.g_ep, self.g_ep_r, ep_r, self.res_queue, self.name)
                        break
                state = next_state
                total_step += 1
        self.res_queue.put(None)

class SharedAdam(torch.optim.Adam):
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.9), eps=1e-8,
                 weight_decay=0):
        super(SharedAdam, self).__init__(params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        # State initialization
        for group in self.param_groups:
            for p in group['params']:
                state = self.state[p]
                state['step'] = 0
                state['exp_avg'] = torch.zeros_like(p.data)
                state['exp_avg_sq'] = torch.zeros_like(p.data)

                # share in memory
                state['exp_avg'].share_memory_()
                state['exp_avg_sq'].share_memory_()

def v_wrap(np_array, dtype=np.float32):
    if np_array.dtype != dtype:
        np_array = np_array.astype(dtype)
    return torch.from_numpy(np_array)

def set_init(layers):
    for layer in layers:
        nn.init.normal_(layer.weight, mean=0., std=0.1)
        nn.init.constant_(layer.bias, 0.)

def push_and_pull(opt, lnet, gnet, done, s_, bs, ba, br, gamma):
    if done:
        v_s_ = 0.               # terminal
    else:
        v_s_ = lnet.forward(v_wrap(s_[None, :]))[-1].data.numpy()[0, 0]

    buffer_v_target = []
    #for r in br[::-1]:    # reverse buffer r
    for r in reversed(br):    # reverse buffer r
        v_s_ = r + gamma * v_s_
        # append() + reversed() is faster than insert(), see https://stackoverflow.com/questions/7776938/python-insert-vs-append
        buffer_v_target.append(v_s_) 
    buffer_v_target.reverse()

    loss = lnet.loss_func(
        v_wrap(np.vstack(bs)),
        v_wrap(np.array(ba), dtype=np.int64) if ba[0].dtype == np.int64 else v_wrap(np.vstack(ba)),
        v_wrap(np.array(buffer_v_target)[:, None]))

    # calculate local gradients and push local parameters to global
    opt.zero_grad()
    loss.backward()
    for lp, gp in zip(lnet.parameters(), gnet.parameters()):
        gp._grad = lp.grad
    opt.step()

    # pull global parameters
    lnet.load_state_dict(gnet.state_dict())


def record(trial, global_ep, global_ep_r, ep_r, res_queue, name):
    with global_ep.get_lock():
        global_ep.value += 1
    #with global_ep_r.get_lock():
    #    if global_ep_r.value == 0.:
    #        global_ep_r.value = ep_r
    #    else:
    #        global_ep_r.value = global_ep_r.value * 0.99 + ep_r * 0.01
    #res_queue.put(global_ep_r.value)
    res_queue.put(ep_r)
    #print(name, "Ep:", global_ep.value, "| Ep_r: %.4f" % global_ep_r.value,)
    print('trial', trial, name, "Ep:", global_ep.value, "| Ep_r: %.4f" % (ep_r/MAX_TICKS))

def save_model(path, model):
    file = open(path, 'wb')
    pickle.dump(model, file)
    file.close()

def run_trial(trial, out_path):
    gnet = Net(num_state_variables, num_actions) # global network
    gnet.share_memory()         # share the global parameters in multiprocessing
    opt = SharedAdam(gnet.parameters(), lr=0.0001)      # global optimizer
    global_ep = mp.Value('i', 0)
    global_ep_r = mp.Value('d', 0.)
    res_queue = mp.Queue()

    # parallel training
    start_time = datetime.now()
    
    workers = [Worker(trial, gnet, opt, global_ep, global_ep_r, res_queue, i) for i in range(num_workers)]
    [w.start() for w in workers]
    res = [] # record episode reward to plot
    while True:
        r = res_queue.get()
        if r is not None:
            res.append(r)
        else:
            break
    [w.join() for w in workers]
    end_time = datetime.now()
    delta = end_time - start_time
    print('Trial', 0, ', A3C learning 2 took ' + str(delta.total_seconds()) + ' seconds')
    
    plot = False
    if plot:
        import matplotlib.pyplot as plt
        plt.plot(res)
        plt.ylabel('Moving average ep reward')
        plt.xlabel('Step')
        plt.show()
    score_file = open(out_path + '/viper-all-scores-' + str(trial).zfill(2) + '.txt', 'w')
    for i in range(1, len(res)):
        score_file.write(str(i) + ',' + str(res[i - 1]/MAX_TICKS) + '\n')
    score_file.close()
    model_path = out_path + '/model' + str(trial).zfill(2) + '-' + str(NUM_EPISODES) + '.p'
    save_model(model_path, gnet)
                        
if __name__ == "__main__":
    os.environ["OMP_NUM_THREADS"] = "1"
    #os.environ['CUDA_VISIBLE_DEVICES'] = ""
    

    out_path = 'rl_results/' + scenario_name
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    print('start:', datetime.now().strftime('%d/%m/%y %H:%M:%S'))

    NUM_TRIALS = 10
    times_file = open(out_path + '/times.txt', 'a+')
    for trial in range(NUM_TRIALS):
        print('\ntrial', trial)
        #env.seed(trial)
        np.random.seed(trial)
        start_time = datetime.now()
        run_trial(trial, out_path)
        end_time = datetime.now()
        delta = end_time - start_time
        times_file.write('=== trial ' + str(trial) + '\n')
        times_file.write('Learning took ' + str(delta.total_seconds()) + ' seconds\n\n')
    print('end:', datetime.now().strftime('%d/%m/%y %H:%M:%S'))
    times_file.close()