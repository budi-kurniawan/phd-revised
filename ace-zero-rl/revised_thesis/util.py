import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
from collections import namedtuple
import random
from scipy.stats import bootstrap


BehaviourDataSource = namedtuple('BehaviourDataSource', 'label data_parent_path num_trials', defaults=[None, None])
context = {'palette': 'Blues', 'baseline_color': 'red', 'figsize': (15, 5), 'legend_loc' : "upper center",
            'distance_btw_agents':0.09}
""" info about the palette: http://seaborn.pydata.org/tutorial/color_palettes.html """

seed = 300_000
rng = np.random.default_rng(seed)
behaviours = ('defensive', 'head-on', 'neutral', 'offensive')

class ScipyBootstrap:
    def __init__(self) -> None:
        self.mean = None

    def calculate_mean(self, sample, axis=0):
        self.mean = np.mean(sample, axis=axis)
        return self.mean

    def execute_with_errors(self, sample, resample_size, method):
        sample = (sample,)  # samples must be in a sequence
        res = bootstrap(sample, self.calculate_mean, confidence_level=0.95, method=method, 
            random_state=rng, n_resamples=resample_size)
        ci = res.confidence_interval
        if method != 'basic':
            mean = np.mean(self.mean)
            error = (mean - ci.low, ci.high - mean)
            return mean, error
        return None, None

def draw_error_bars(data_sources, result_path=None):
    plt.rcParams["figure.figsize"] = context['figsize']
    data = []
    baselines = []
    legend_labels = []
    offset = 0.5
    for ds in data_sources:
        label = ds.label
        if label!='baseline':
            legend_labels.append(label)
        for trial in range(10):
            file = ds.data_parent_path + '/values-by-behaviour-' + str(trial).zfill(2) + '.txt'
            if not os.path.exists(file):
                if label!='baseline':
                    print(file + " does not exist.")
                break
            with open(file,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter=',')
                for row in plots:
                    sample = {'behaviour': row[0], 'value': float(row[1]) + offset, 'label':label}
                    if label=='baseline':
                        baselines.append(sample)
                    else:
                        data.append(sample)
    # at this point, data contains all samples from all data sources, 
    # 40 samples (10 for each behaviour) from each source * num_data_sources

    x_1 = np.arange(1, 5)
    distance_btw_agents = context['distance_btw_agents']
    colors = context['palette']
    for index, label in enumerate(legend_labels):
        y = []
        errors = []
        agent_data = [x for x in data if x['label']==label]
        for behaviour in ['defensive', 'head-on', 'neutral', 'offensive']:
            values = [x['value'] for x in agent_data if x['behaviour']==behaviour]
            mean, error = ScipyBootstrap().execute_with_errors(values, 10000, 'bca')
            y.append(mean)
            errors.append(error)
        errors = np.array(errors).T
        y = np.array(y)
        plt.errorbar(x=x_1, y=y, yerr=errors, color='gray', capsize=3,
            linestyle="None", marker="s", markersize=7, mfc=colors[index], mec="black", label=label)
        x_1 = x_1 + distance_btw_agents

    x_ticks = ('defensive', 'head-on', 'neutral', 'offensive')
    # adjust x_1 so it is in the middle
    x_1 = x_1 - (len(legend_labels) + 1)* distance_btw_agents / 2
    plt.xticks(x_1, x_ticks, rotation=0)

    if 'legend_loc' in context:
        plt.legend(loc=context['legend_loc'], ncol=context['legend_num_columns'])
    else:
        plt.legend(loc='upper center', ncol=context['legend_num_columns'])

    baseline_width = len(legend_labels) * distance_btw_agents
    for i, behaviour in enumerate(behaviours):
        baseline_value = [e for e in baselines if e['behaviour'] == behaviour][0]['value']
        plt.plot([-baseline_width/2 + x_1[i], baseline_width/2 + x_1[i]], [baseline_value, baseline_value], linewidth=2, 
            color=context['baseline_color'], zorder=0.5)
    plt.xlabel('Blue UAV initial disposition', fontsize=11)
    plt.ylabel('Average Reward', fontsize=11)
    if 'ylim' in context:
        plt.ylim(context['ylim'])
    plt.grid(axis='y')
    plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced 
    if result_path is not None:
        plt.savefig(result_path)       
    plt.show()