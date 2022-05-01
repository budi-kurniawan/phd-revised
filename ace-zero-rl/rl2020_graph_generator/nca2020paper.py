import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
import numpy as np


def draw(path, image_path, palette=None):
    sns.set(style="whitegrid")
    dataFrame = pd.read_csv(path, sep=',')
    print(dataFrame)
    
    ax = sns.boxplot(data=dataFrame, whis=np.inf, width=0.6, palette=palette)
    ax = sns.swarmplot(data=dataFrame, color=".2")
    #handles, _ = bplot.get_legend_handles_labels()
    #bplot.legend(handles, legend_labels)#    facecolors = ('orange', 'lightblue', 'lightgreen', 'green', 'lightyellow', 'lightcyan', 'yellow', 'lightpink', 'red')
# #     artists = bplot.artists
# #     for i in range(len(artists)):
# #         artists[i].set_facecolor(facecolors[i % 8])
 
#     for i in range(len(baselines)):
#         baseline = baselines[i]
#         bplot.plot([-.4 + i, 0.4 + i], [baseline['value'], baseline['value']], linewidth=4, color=context['baseline_color'], zorder=0.5)
    #plt.xlabel('Behaviour')
    plt.ylabel('Average Score')
    plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
    plt.savefig(image_path)
    plt.show()
    
if __name__ == '__main__':
    plt.rcParams["figure.figsize"] = (9, 4)
    plt.rcParams["legend.loc"] = 'upper left'
    parent_path = 'C:/Users/jayden/Desktop/PHD/my-papers/neuralComputingAndApplications/results'
    
#     for i in range(1, 5):
#         data_path = parent_path + '/d2dspl-aircombat-test' + str(i) + '.txt'
#         plot_path = parent_path + '/d2dspl-aircombat-test' + str(i) + '.png'
#         draw(data_path, plot_path)
# 
#     plt.rcParams["figure.figsize"] = (6, 4)
#     for i in range(1, 5):
#         data_path = parent_path + '/d2dsql-aircombat-test' + str(i) + '.txt'
#         plot_path = parent_path + '/d2dsql-aircombat-test' + str(i) + '.png'
#         draw(data_path, plot_path)

    plt.rcParams["figure.figsize"] = (9, 4)
    
    palette = ['#FCFABE', '#FCFABE', 'lightblue', 'lightgreen', 'lightgreen', '#fcfafa', '#fcfafa', '#fcfafa', '#fcfafa', '#fcfafa', '#fcfafa']
    for i in range(1, 5):
        data_path = parent_path + '/d2dspl-d2dsql-aircombat-test' + str(i) + '.txt'
        plot_path = parent_path + '/d2dspl-d2dsql-aircombat-test' + str(i) + '.png'
        plt.xticks(rotation='vertical')
        draw(data_path, plot_path, palette)
