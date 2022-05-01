import os
import matplotlib.pyplot as plt
import csv
import socket
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override
from enum import Enum

class RewardType(Enum):
    AVERAGE = 1
    TOTAL = 2
    NUM_STEPS = 3
    REDEFINED = 4

class FileLogListener(TrialListener, EpisodeListener):
    def __init__(self, chart_offset, reward_type=RewardType.AVERAGE):
        self.reward_type = reward_type
        self.scores_file = None
        self.writer = None
        self.chart_offset = chart_offset

    @override(EpisodeListener)
    def after_episode(self, event):
        episode = event.activity_context.episode
        step = event.activity_context.step
        if self.scores_file is not None:
            if self.reward_type == RewardType.NUM_STEPS:
                self.scores_file.write(str(episode) + "," + str(step) + '\n')
            elif self.reward_type == RewardType.AVERAGE:
                self.scores_file.write(str(episode) + "," + str(event.avg_reward) + '\n')
            elif self.reward_type == RewardType.TOTAL:
                self.scores_file.write(str(episode) + "," + str(event.reward) + '\n')
            elif self.reward_type == RewardType.REDEFINED:
                self.scores_file.write(str(episode) + "," + str(event.agent.total_redefined_reward/step) + '\n')
                
    @override(TrialListener)
    def before_trial(self, event):
        out_path = event.activity_context.out_path
        trial = event.activity_context.trial
        self.scores_file = open(out_path + '/all-scores-' + str(trial).zfill(2) + '.txt', 'a+')

    @override(TrialListener)
    def after_trial(self, event):
        self.scores_file.close()
        ac = event.activity_context
        out_path = ac.out_path
        trial = ac.trial
        duration_in_seconds = (ac.trial_end_time - ac.trial_start_time).total_seconds()
        times_file = open(out_path + '/learning-times.txt', 'a+')
        msg = 'Trial ' + str(trial) + ' finished in ' + str(duration_in_seconds) + ' seconds on ' + socket.gethostname()
        times_file.write(msg + '\n')
        times_file.close()
        self.draw_chart(trial, out_path)

    def draw_chart(self, trial, out_path):
        plt.rcParams["figure.figsize"] = (20, 4)
        plt.rcParams["legend.loc"] = 'lower center'
        scores_path = out_path + '/all-scores-' + str(trial).zfill(2) + '.txt'        
        x = []
        y = []
        offset = self.chart_offset
        with open(scores_path, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                x.append(int(row[0]))
                y.append(float(row[1]) + offset)
        plt.plot(x, y)
        plt.xlabel('Episode')
        plt.ylabel('Total score')
        plt.savefig(scores_path + '.png')
        plt.close()