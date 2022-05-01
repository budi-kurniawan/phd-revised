import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import csv
import os
import numpy as np
from collections import namedtuple
from matplotlib.ticker import FuncFormatter

DataSource = namedtuple('DataSource', 'name data_paths result_path labels image_path image_xy title', defaults=[None, None, None])
context = {'num_trials': 10, 'max_records': 100_000, 'num_avg_samples': 250, 'offset': 0.5, 'start_trial':0,
           'figsize': (14, 3), 'show_figures': False, 'ylim': (0, .8), 'legend.loc': 'upper left',
           'colors':['blue', 'orange', 'green', 'red'],
           'edgecolors':['lightblue', 'coral', 'green', 'red'],
           'facecolors':['lightblue', 'coral', 'green', 'red']
}

def get_data(num_trials, path, max_records, num_avg_samples, offset):
    X = []
    Y = []
    start_trial = context['start_trial']
    for i in range(start_trial, start_trial + num_trials):
        file = path + '/all-scores-0' + str(i) + '.txt'
        # allow this function to use a smaller number of data sources
        if not os.path.exists(file):
            print(file + ' does not exist. Use existing data only.')
            break 
        x = []
        y = []
        with open(file,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                x.append(int(row[0]))
                y.append(float(row[1]) + offset)
                if len(y) == max_records:
                    break
    
        if num_avg_samples != 1:
            for j in range(0, int(len(x)/num_avg_samples)):
                x[j] = x[(j + 1) * num_avg_samples - 1]
                index = j * num_avg_samples
                y[j] = np.mean(y[index : index + num_avg_samples])
            x = x[0 : int(len(x)/num_avg_samples)]
            y = y[0 : len(x)]
        X.append(x)
        Y.append(y)
    return X, Y

def draw(axs, data_paths, labels):
    for i in range(len(data_paths)):
        X, Y = get_data(context['num_trials'], data_paths[i], context['max_records'], context['num_avg_samples'], context['offset'])
        all_runs = np.stack(Y)
        means = np.mean(all_runs, axis=0)
        stddev = np.std(all_runs, axis=0)
        label = labels[i] + ' ({0:.4f})'.format(np.mean(means)) 
        axs.plot(X[0], means, color=context['colors'][i], label=label) # no std
        axs.fill_between(X[0], means-stddev, means+stddev, alpha=0.2, edgecolor=context['edgecolors'][i], 
                        facecolor=context['facecolors'][i], linewidth=2, linestyle='dashdot', antialiased=True)
        #plt.errorbar(X[0], means, stddev, linestyle='None', marker='.', label=labels[i])

def add_image(ax, data_source):
    if data_source.image_path is None:
        return
    artist_array = mpimg.imread(data_source.image_path)
    imagebox = OffsetImage(artist_array, zoom=0.5)
    ab = AnnotationBbox(imagebox, xy=data_source.image_xy, xybox=(0, 0), xycoords='data', boxcoords=("offset points"), box_alignment=(0, 1), pad=0.5)
    ax.add_artist(ab)

def get_axis_dim(fig, ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    arrow_width, height = bbox.width, bbox.height
    arrow_width *= fig.dpi
    height *= fig.dpi
    return arrow_width, height
    
def create_charts(data_sources):
    plt.rcParams["figure.figsize"] = context['figsize']
    plt.rcParams["legend.loc"] = context['legend.loc']
    for data_source in data_sources:
        fig, axs = plt.subplots(1)
        axs.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
        axs.set_ylim(context['ylim'])
        plt.margins(0, x=None, y=None, tight=True)
#         plt.xlabel('Episode')
#         plt.ylabel('Average Reward')
        axs.set_xlabel('Episode', fontsize=15)
        axs.set_ylabel('Average Reward', fontsize=15)
        if data_source.title is not None:
            axs.text(.5,.9, data_source.title, horizontalalignment='center', transform=axs.transAxes, 
                    fontsize=13)
            
        draw(axs, data_source.data_paths, data_source.labels)
        add_image(axs, data_source)
        axs.legend()
        plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
        print(' Saved ' + data_source.result_path)
        plt.savefig(data_source.result_path)
        if context['show_figures']:
            plt.show()
            
if __name__ == '__main__':
    num_trials=1
    parent = '../rl2020_results/'

    path = parent + 'temp'
    max_records = 1000_0000
    num_rewards = 1
    context['num_trials'] = 2
    context['num_avg_samples'] = 2
    context['offset'] = 0
    context['show_figures'] = True
    context['ylim'] = (0, 10)
    
    data_sources = [
            DataSource(name='ac-001', data_paths=[parent + 'temp'], labels=['ac-001', 'ac-002'],
                       image_path=None, image_xy=None, result_path='./temp/temp-01.png')
    ]
    
    #X, Y = get_mo_data(num_trials, path, max_records, num_avg_samples, offset, num_rewards)
    #print('X:', X)
    #print('===================')
    #print(Y)
    create_charts(data_sources)            