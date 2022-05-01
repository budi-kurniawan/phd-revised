import os
import matplotlib.pyplot as plt
import csv
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override

class TestResultLogger(TrialListener, EpisodeListener):
    def __init__(self, chart_offset, use_num_steps_as_reward=False):
        self.use_num_steps_as_reward = use_num_steps_as_reward
        self.scores_file = None
        self.writer = None
        self.chart_offset = chart_offset

    @override(EpisodeListener)
    def after_episode(self, event):
        if self.scores_file is not None:
            activity_context = event.activity_context
            episode = activity_context.episode
            step = activity_context.step
            if self.use_num_steps_as_reward:
                self.scores_file.write(str(episode) + "," + str(step) + '\n')
            else:
                self.scores_file.write(str(episode) + "," + str(event.avg_reward) + '\n')
                
    @override(TrialListener)
    def before_trial(self, event):
        out_path = event.activity_context.out_path
        trial = event.activity_context.trial
        self.scores_file = open(out_path + '/all-scores-' + str(trial).zfill(2) + '.txt', 'w')

    @override(TrialListener)
    def after_trial(self, event):
        self.scores_file.close()
        ac = event.activity_context
        out_path = ac.out_path
        trial = ac.trial
        duration_in_seconds = (ac.trial_end_time - ac.trial_start_time).total_seconds()
        times_file = open(out_path + '/times.txt', 'a+')
        msg = 'Trial ' + str(trial) + ' finished in ' + str(duration_in_seconds) + ' seconds.'
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
        plt.plot(x, y, 'bo')
        plt.axis([1, len(x), 0, 1])
        plt.xlabel('Test')
        plt.ylabel('Total score')
        plt.savefig(scores_path + '.png')
        plt.close()