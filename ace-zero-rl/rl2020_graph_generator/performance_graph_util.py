import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
from collections import namedtuple

BehaviourDataSource = namedtuple('BehaviourDataSource', 'label data_parent_path num_trials', defaults=[None, None])
context = {'palette': 'Blues', 'baseline_color': 'red', 'figsize': (15, 5), 'legend_loc' : "upper center"}
""" info about the palette: http://seaborn.pydata.org/tutorial/color_palettes.html """

def draw(data_sources, result_path=None):
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
    
    sns.set(style="whitegrid")
    dataFrame = pd.DataFrame(data)
    bplot = sns.boxplot(x="behaviour", y="value", hue="label", data=dataFrame, whis=np.inf, width=0.6, palette=context['palette'])
    #bplot = sns.boxplot(x="behaviour", y="value", hue="label", data=dataFrame, palette=context['palette'])
    # currently cannot show data points as this is a 'bug': https://github.com/mwaskom/seaborn/issues/941
    #ax = sns.swarmplot(x="behaviour", y="value", data=dataFrame, color=".25")
    
    #bplot = sns.swarmplot(x="behaviour", y="value", hue="label", data=dataFrame, color=".2")

    handles, _ = bplot.get_legend_handles_labels()
    bplot.legend(handles, legend_labels)#    facecolors = ('orange', 'lightblue', 'lightgreen', 'green', 'lightyellow', 'lightcyan', 'yellow', 'lightpink', 'red')
    plt.legend(loc=context['legend_loc'])
#     plt.legend(loc='best', bbox_to_anchor=(0.3, 0.2))

#     artists = bplot.artists
#     for i in range(len(artists)):
#         artists[i].set_facecolor(facecolors[i % 8])

    for i in range(len(baselines)):
        baseline = baselines[i]
        bplot.plot([-.4 + i, 0.4 + i], [baseline['value'], baseline['value']], linewidth=4, color=context['baseline_color'], zorder=0.5)
#     plt.xlabel('Blue UAV initial disposition')
#     plt.ylabel('Average Reward')
    bplot.set_xlabel('Blue UAV initial disposition', fontsize=15)
    bplot.set_ylabel('Average Reward', fontsize=15)
    if 'ylim' in context:
        plt.ylim(context['ylim'])
    plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
    if result_path is not None:
        plt.savefig(result_path)
    plt.show()
