import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import csv
import os
import numpy as np
from collections import namedtuple
from matplotlib.ticker import FuncFormatter
from turtledemo.__main__ import font_sizes

DataSource = namedtuple('DataSource', 'name data_paths result_path labels num_rewards title image_path image_xy', defaults=[None, None])
context = {'num_trials': 10, 'max_records': 100_000, 'num_avg_samples': 250, 'offset': 0.5, 
        'show_figures': False, 'ylim': (0, 1), 'title_color':'brown', 'draw_line': False, 'line_color':'grey'}

def get_data(num_trials, path, max_records, num_avg_samples, offset, reward_no):
    X = []
    Y = []
    for i in range(num_trials):
        file = path + '/mo-scores-0' + str(i) + '.txt'
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
                y.append(float(row[reward_no]) + offset)
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

def draw(axs, data_paths, labels, num_rewards):
    colors = ['blue', 'orange', 'green']
    edgecolors = ['lightblue', 'coral', 'green']
    facecolors = ['lightblue', 'coral', 'green']
    
    for i in range(num_rewards):
        X, Y = get_data(context['num_trials'], data_paths[0], context['max_records'], context['num_avg_samples'], context['offset'], i+1)
        all_runs = np.stack(Y)
        means = np.mean(all_runs, axis=0)
        stddev = np.std(all_runs, axis=0)
        label = labels[i] + ' ({0:.4f})'.format(np.mean(means)) 
        axs.plot(X[0], means, color=colors[i], label=label) # no std
        if context['draw_line']:
            axs.plot([0, context['max_records']], [0, 0], linewidth=1, color=context['line_color'], zorder=0.5)

        axs.fill_between(X[0], means-stddev, means+stddev, alpha=0.2, edgecolor=edgecolors[i], facecolor=facecolors[i],
                         linewidth=2, linestyle='dashdot', antialiased=True)

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
    plt.rcParams["figure.figsize"] = (15, 4)
    plt.rcParams["legend.loc"] = 'upper left'
    for data_source in data_sources:
        if os.path.exists(data_source.result_path):
            print(data_source.result_path + ' already exists. Skip it')
            continue
        fig, axs = plt.subplots(1)
        axs.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
        axs.set_ylim(context['ylim'])
        plt.margins(0, x=None, y=None, tight=True)
#         plt.xlabel('Episode')
#         plt.ylabel('Average Score')
        axs.set_xlabel('Episode', fontsize=15)
        axs.set_ylabel('Average Reward', fontsize=15)
        axs.text(.5,.9,data_source.title, horizontalalignment='center', transform=axs.transAxes, 
                 color=context['title_color'], size=13, weight='bold')
        draw(axs, data_source.data_paths, data_source.labels, data_source.num_rewards)
        add_image(axs, data_source)
        axs.legend()
        plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
        plt.savefig(data_source.result_path)
        if context['show_figures']:
            plt.show()
            
            
if __name__ == "__main__":
    context['show_figures'] = False
    parent_ql = '../rl2021_mo_results/ql-mo/'
    parent_ac = '../rl2021_mo_results/ac-mo/'
    parent_dqn_shared = '../rl2021_mo_results/dqn-mo-shared/'
    parent_dqn_mnn = '../rl2021_mo_results/dqn-mo-mnn/'

    image_paths = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (14000, 0.96)
    out_path = './mo-learning-curves/'

    context['max_records'] = 200_000
    context['num_trials'] = 10
    context['num_avg_samples'] = 250
    context['offset'] = 0
    labels = ['reward 1', 'reward 2', 'reward 3']
    num_rewards = len(labels)
    
    ''' MO-Q(lambda) learning curves RB001-RB003'''
    data_sources = [
            DataSource(name='ql-001-rb001', data_paths=[parent_ql + 'ql-mo-001-200000-rb001'], labels=labels, 
                title='Multiobjective Q($\lambda$) with RB001', num_rewards=3, result_path=out_path + 'ql-mo-001-200000-rb001.pdf'),
            DataSource(name='ql-random-rb002', data_paths=[parent_ql + 'ql-mo-random-200000-rb002'], labels=labels, 
                title='Multiobjective Q($\lambda$) with RB002', num_rewards=3, result_path=out_path + 'ql-mo-random-200000-rb002.pdf'),
            DataSource(name='ql-random-rb002', data_paths=[parent_ql + 'ql-mo-random-200000-rb003'], labels=labels, 
                title='Multiobjective Q($\lambda$) with RB003', num_rewards=3, result_path=out_path + 'ql-mo-random-200000-rb003.pdf'),
    ]    
#     create_charts(data_sources)                
    
    ''' MO-ACET learning curves RB001-RB003'''    
    data_sources = [
            DataSource(name='ac-random', data_paths=[parent_ac + 'ac-mo-random-500000-rb001'], labels=labels, 
                title='Multiobjective ACET with RB001', num_rewards=3, result_path=out_path + 'ac-mo-random-20000-rb001.pdf'),
            DataSource(name='ac-random-rb002', data_paths=[parent_ac + 'ac-mo-random-200000-rb002'], labels=labels,
               title='Multiobjective ACET with RB002', num_rewards=3, result_path=out_path + 'ac-mo-random-20000-rb002.pdf'),
            DataSource(name='ac-random-rb003', data_paths=[parent_ac + 'ac-mo-random-200000-rb003'], labels=labels,
               title='Multiobjective ACET with RB003', num_rewards=3, result_path=out_path + 'ac-mo-random-20000-rb003.pdf'),
        ]
#     create_charts(data_sources)
    
    ''' MO-ACET learning curves RB011-RB016'''
    context['max_records'] = 200_000
    context['num_trials'] = 10
    context['num_avg_samples'] = 250
    context['offset'] = 0
    context['show_figures'] = False
    context['draw_line'] = True
    context['ylim'] = (-0.1, 0.4)
    data_sources = [
            DataSource(name='ac-001', data_paths=[parent_ac + 'ac-mo-random-500000-rb013'], labels=labels, 
                title='Multiobjective ACET with RB004', num_rewards=2, result_path=out_path + 'ac-mo-random-20000-rb004.pdf'),
            DataSource(name='ac-001', data_paths=[parent_ac + 'ac-mo-random-500000-rb014'], labels=labels, 
                title='Multiobjective ACET with RB005', num_rewards=2, result_path=out_path + 'ac-mo-random-20000-rb005.pdf'),
            DataSource(name='ac-001', data_paths=[parent_ac + 'ac-mo-random-500000-rb015'], labels=labels, 
                title='Multiobjective ACET with RB006', num_rewards=2, result_path=out_path + 'ac-mo-random-20000-rb006.pdf'),
            DataSource(name='ac-001', data_paths=[parent_ac + 'ac-mo-random-500000-rb016'], labels=labels, 
                title='Multiobjective ACET with RB007', num_rewards=2, result_path=out_path + 'ac-mo-random-20000-rb007.pdf'),
    ]    
    create_charts(data_sources)                
    context['draw_line'] = False
    
    
    ''' MO DQN shared learning '''
    data_sources = [
        DataSource(name='dqn-random', data_paths=[parent_dqn_shared + 'dqn-mo-shared-random-20000-rb001'], labels=labels, 
            title='Multiobjective DQN (shared network) with RB001', num_rewards=3, result_path=out_path + 'dqn-mo-shared-random-20000-rb001.pdf'),
        DataSource(name='dqn-002', data_paths=[parent_dqn_shared + 'dqn-mo-shared-random-20000-rb002'], labels=labels, 
            title='Multiobjective DQN (shared network) with RB002', num_rewards=3, result_path=out_path + 'dqn-mo-shared-random-20000-rb002.pdf'),
        DataSource(name='dqn-003', data_paths=[parent_dqn_shared + 'dqn-mo-shared-random-20000-rb003'], labels=labels, 
            title='Multiobjective DQN (shared network) with RB003', num_rewards=3, result_path=out_path + 'dqn-mo-shared-random-20000-rb003.pdf'),
    ]    
#     create_charts(data_sources)                

    ''' MO DQN MNN learning '''
#     context['max_records'] = 20_000
    data_sources = [
        DataSource(name='dqn-r-rb001', data_paths=[parent_dqn_mnn + 'dqn-mo-mnn-random-20000-rb001'], labels=labels, 
            title='Multiobjective DQN (multinetworks) with RB001', num_rewards=3, result_path=out_path + 'dqn-mo-mnn-random-20000-rb001.pdf'),
        DataSource(name='dqn-r-rb002', data_paths=[parent_dqn_mnn + 'dqn-mo-mnn-random-20000-rb002'], labels=labels, 
            title='Multiobjective DQN (multinetworks) with RB002', num_rewards=3, result_path=out_path + 'dqn-mo-mnn-random-20000-rb002.pdf'),
        DataSource(name='dqn-r-rb003', data_paths=[parent_dqn_mnn + 'dqn-mo-mnn-random-20000-rb003'], labels=labels, 
            title='Multiobjective DQN (multinetworks) with RB003', num_rewards=3, result_path=out_path + 'dqn-mo-mnn-random-20000-rb003.pdf'),
    ]    
    create_charts(data_sources)                
