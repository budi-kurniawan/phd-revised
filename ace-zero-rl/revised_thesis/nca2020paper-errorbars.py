import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np
from util import *
import os
os.system('cls' if os.name == 'nt' else 'clear')

def draw(path, image_path, palette=None):
    sns.set(style="whitegrid")
    dataFrame = pd.read_csv(path, sep=',')
    print(dataFrame)    
    ax = sns.boxplot(data=dataFrame, whis=np.inf, width=0.6, palette=palette)
    ax = sns.swarmplot(data=dataFrame, color=".2")
    plt.ylabel('Average Score')
    plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
    #plt.savefig(image_path)
    plt.show()
    
if __name__ == '__main__':
    plt.rcParams["figure.figsize"] = (9, 4)
    plt.rcParams["legend.loc"] = 'upper left'
    parent_path = './ace-zero-rl/rl2020_test_results/nca_paper'    
    plt.rcParams["figure.figsize"] = (9, 4)
    
    palette = ['#FCFABE', '#FCFABE', 'lightblue', 'lightgreen', 'lightgreen', '#fcfafa', '#fcfafa', '#fcfafa', '#fcfafa', '#fcfafa', '#fcfafa']
    for i in range(1, 5):
        data_path = parent_path + '/d2dspl-d2dsql-aircombat-test' + str(i) + '.txt'
        plot_path = parent_path + '/d2dspl-d2dsql-aircombat-test' + str(i) + '.png'
        print('data path:', os.path.abspath(data_path))
        plt.xticks(rotation='vertical')
        draw(data_path, plot_path, palette)
