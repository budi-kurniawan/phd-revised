import seaborn as sns
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


def bootstrap(x, n, repeats, seed):
    x = np.array(x)
    sample_mean = []
    pctl25 = []
    pctl50 = []
    pctl75 = []
    random.seed(seed)
    for i in range(repeats):
        y = random.sample(x.tolist(), n)
        # print("y:", y)
        avg = np.mean(y)
        sample_mean.append(np.mean(y))
        pctl25.append(np.percentile(y, 2.5))
        pctl50.append(np.percentile(y, 50))
        pctl75.append(np.percentile(y, 97.5))
    return sample_mean, pctl25, pctl50, pctl75

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
    
    print('data:', len(data))

    data_defensive = [sample['value'] for sample in data if sample['behaviour']=='defensive']
    data_head_on = [sample['value'] for sample in data if sample['behaviour']=='head-on']
    data_neutral = [sample['value'] for sample in data if sample['behaviour']=='neutral']
    data_offensive = [sample['value'] for sample in data if sample['behaviour']=='offensive']
    print('defensive:', data_defensive)
    print('defensive mean:', np.mean(data_defensive))
    n = 5
    repeats = 10_000
    seed = 300_000
    sample_mean, pctl25, pctl50, pctl75 = bootstrap(data_defensive, n, repeats, seed)
    print("bootstrap mean:", np.mean(sample_mean))
    # print('head-on:', data_head_on)
    # print('neutral:', data_neutral)
    # print('offensive:', data_offensive)


    return
    sns.set(style="whitegrid")
    dataFrame = pd.DataFrame(data)
    bplot = sns.boxplot(x="behaviour", y="value", hue="label", data=dataFrame, whis=np.inf, width=0.6, palette=context['palette'])
    handles, _ = bplot.get_legend_handles_labels()
    bplot.legend(handles, legend_labels)#    facecolors = ('orange', 'lightblue', 'lightgreen', 'green', 'lightyellow', 'lightcyan', 'yellow', 'lightpink', 'red')
    plt.legend(loc=context['legend_loc'])
    for i in range(len(baselines)):
        baseline = baselines[i]
        bplot.plot([-.4 + i, 0.4 + i], [baseline['value'], baseline['value']], linewidth=4, color=context['baseline_color'], zorder=0.5)
    bplot.set_xlabel('Blue UAV initial disposition', fontsize=15)
    bplot.set_ylabel('Average Reward', fontsize=15)
    if 'ylim' in context:
        plt.ylim(context['ylim'])
    plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
    if result_path is not None:
        plt.savefig(result_path)
    plt.show()
