import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
from collections import namedtuple
import random


BehaviourDataSource = namedtuple('BehaviourDataSource', 'label data_parent_path num_trials', defaults=[None, None])
context = {'palette': 'Blues', 'baseline_color': 'red', 'figsize': (15, 5), 'legend_loc' : "upper center"}
""" info about the palette: http://seaborn.pydata.org/tutorial/color_palettes.html """

seed = 300_000
rng = np.random.default_rng(seed)


def my_bootstrap_with_errors(x, num_resamples=5, iteration=10000):
    # confidence level: 0.95
    random.seed(seed)
    x = np.array(x)
    resample_mean = []
    pctl_2_5 = []
    pctl_97_5 = []
    for i in range(iteration):
        y = random.choices(x.tolist(), k=num_resamples)
        resample_mean.append(np.mean(y))
        pctl_2_5.append(np.percentile(y, 2.5))
        pctl_97_5.append(np.percentile(y, 97.5))
    mean = np.mean(resample_mean)
    lower_error = mean - np.mean(pctl_2_5)
    upper_error = np.mean(pctl_97_5) - mean
    return mean, (lower_error, upper_error)

def my_bootstrap2_with_errors(x, num_resamples=10, iteration=10000):
    # inspired by https://allendowney.github.io/ElementsOfDataScience/12_bootstrap.html
    # confidence level: 0.95
    random.seed(seed)
    x = np.array(x)
    resample_means = []
    for i in range(iteration):
        y = random.choices(x.tolist(), k=num_resamples)
        resample_means.append(np.mean(y))
    ci = np.percentile(resample_means, [2.5, 97.5])
    mean = np.mean(resample_means)
    lower_error = mean - ci[0]
    upper_error = ci[1] - mean
    return mean, (lower_error, upper_error)


def draw_line_charts(data_sources, result_path=None):
    plt.rcParams["figure.figsize"] = context['figsize']
    data = []
    baselines = []
    legend_labels = []
    offset = 0.5
    for ds in data_sources:
        label = ds.label
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
    iteration = 100
    index = 0
    colors = ['#efffef', '#ccffe0', '#b2ffd0', '#99ffc1', '#00ff64', '#fff9b2', 'orange'] #https://www.w3schools.com/colors/colors_gradient.asp
    for label in legend_labels:
        y = []
        errors = []
        agent_data = [x for x in data if x['label']==label]
        for behaviour in ['defensive', 'head-on', 'neutral', 'offensive']:
            values = [x['value'] for x in agent_data if x['behaviour']==behaviour]
            # resample with bootstrap
            mean, error = my_bootstrap2_with_errors(values, 5, iteration)
            y.append(mean)
            errors.append(error)
        errors = np.array(errors).T
        y = np.array(y)
        plt.errorbar(x=x_1, y=y, yerr=errors, color='gray', capsize=3,
            linestyle="None", marker="s", markersize=7, mfc=colors[index], mec="black", label=label)
        x_1 = x_1 + 0.05
        index = index + 1

    x_ticks = ('defensive', 'head-on', 'neutral', 'offensive')
    # adjust x_1 so it is in the middle
    x_1 = x_1 - (len(legend_labels) + 1)* 0.05 / 2
    plt.xticks(x_1, x_ticks, rotation=90)
    plt.legend(loc='upper center')
    plt.tight_layout()
    plt.show()