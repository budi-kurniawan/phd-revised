import os
import matplotlib.pyplot as plt
import csv
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override
from enum import Enum
from rl2020.listener.impl.file_log_listener import FileLogListener

class RewardType(Enum):
    AVERAGE = 1
    TOTAL = 2
    NUM_STEPS = 3
    REDEFINED = 4

class MultiObjectiveFileLogListener(FileLogListener):
    def __init__(self):
        super().__init__(0)

    @override(FileLogListener)
    def after_episode(self, event):
        if self.scores_file is None:
            return
        agent = event.agent
        episode = event.activity_context.episode
        step = event.activity_context.step
        self.scores_file.write(str(episode) + "," + ','.join(str(x) for x in (agent.total_rewards/step)) + ","
                + str(agent.total_redefined_reward/step) + "," + str(event.avg_reward) + '\n')
                
    @override(FileLogListener)
    def before_trial(self, event):
        trial = event.activity_context.trial
        out_path = event.activity_context.out_path
        self.scores_file = open(out_path + '/mo-scores-' + str(trial).zfill(2) + '.txt', 'a+')

    @override(FileLogListener)
    def draw_chart(self, trial, out_path):
        # skip this one until further
        if os.path.exists(out_path):
            return
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