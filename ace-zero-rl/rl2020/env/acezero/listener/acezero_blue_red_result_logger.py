import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.listener.step_listener import StepListener
from rl2020.util.util import override

""" Log red and blue average mcgrew scores / episode """
class AceZeroBlueRedResultLogger(TrialListener, EpisodeListener, StepListener):
    def __init__(self, chart_offset):
        self.scores_file = None
        self.writer = None
        self.chart_offset = chart_offset

    @override(StepListener)
    def after_step(self, event):
        cobra = event.env_data.get('cobra', None)
        self.red_total_reward += cobra.mcgrew_score        
         
    @override(EpisodeListener)
    def before_episode(self, event):
        self.red_total_reward = 0
         
    @override(EpisodeListener)
    def after_episode(self, event):
        activity_context = event.activity_context
        episode = activity_context.episode
        step = activity_context.step
        avg_red = -0.5 + self.red_total_reward / step # with offset
        #print('episode:', episode, ', step:', step, ', red_total_reward:', self.red_total_reward, ', avg_red:', avg_red)
        self.scores_file.write(str(episode) + "," + str(event.avg_reward) + ',' + str(avg_red) + '\n')
        if event.avg_reward > avg_red:
            self.blue_wins += 1
        if avg_red > event.avg_reward:
            self.red_wins += 1
                
    @override(TrialListener)
    def before_trial(self, event):
        activity_context = event.activity_context
        trial = activity_context.trial
        out_path = activity_context.out_path
        self.scores_file = open(out_path + '/blue-red-scores-' + str(trial).zfill(2) + '.txt', 'w')
        self.blue_wins = 0
        self.red_wins = 0

    @override(TrialListener)
    def after_trial(self, event):
        ac = event.activity_context
        trial = ac.trial
        out_path = ac.out_path
        self.scores_file.write('------------------------\n')
        self.scores_file.write('Blue wins:' + str(self.blue_wins) + ', Red wins:' + str(self.red_wins))
        self.scores_file.close()
        blue_red_wins_file = open(out_path + '/blue-red-wins.txt', 'a+')
        blue_red_wins_file.write('Trial ' + str(trial) + ' & ' + str(self.blue_wins) + ' & ' + str(self.red_wins) + '\\\\\n')
        blue_red_wins_file.close()
        duration_in_seconds = (ac.trial_end_time - ac.trial_start_time).total_seconds()
        times_file = open(out_path + '/times.txt', 'a+')
        msg = 'Trial ' + str(trial) + ' finished in ' + str(duration_in_seconds) + ' seconds.'
        times_file.write(msg + '\n')
        times_file.close()
        #self.draw_chart(trial, out_path)

    def draw_chart(self, trial, out_path):
        plt.rcParams["figure.figsize"] = (20, 4)
        plt.rcParams["legend.loc"] = 'upper left'
        scores_path = out_path + '/blue-red-scores-' + str(trial).zfill(2) + '.txt'        
        x = []; y_blue = []; y_red = []
        offset = self.chart_offset
        blue_wins = 0; red_wins = 0
        with open(scores_path, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                x.append(int(row[0]))
                blue_reward = float(row[1]) + offset
                red_reward = float(row[2]) + offset
                y_blue.append(blue_reward)
                y_red.append(red_reward)
                if blue_reward > red_reward:
                    blue_wins += 1
                if red_reward > blue_reward:
                    red_wins += 1
        blue_label = ' ({0:.4f})'.format(np.mean(y_blue)) + ' wins: ' + str(blue_wins) + '/144'
        red_label = ' ({0:.4f})'.format(np.mean(y_red)) + ' wins: ' + str(red_wins) + '/144'

        plt.plot(x, y_blue, 'bo', label=blue_label)
        plt.plot(x, y_red, 'r+', label=red_label)
        plt.axis([1, len(x), 0, 1])
        plt.xlabel('Test')
        plt.ylabel('Total score')
        plt.legend()
        plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
        plt.savefig(scores_path + '.png')
        plt.close()
