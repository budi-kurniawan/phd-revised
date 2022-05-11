import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
from collections import namedtuple
from util import *

os.system('cls' if os.name == 'nt' else 'clear')

DataSource = namedtuple('DataSource', 'name data_parent_path num_episodes multiplier', defaults=[None, None])
context = {'figsize': (5, 4), 'xlabel':'', 'ylabel':'', 'show_figures': False, 'ylim': (0, 1), 
        'distance_btw_agents': 0.09}
context['use_ltpe'] = False # ltpe = learning time per episode
context['table_caption'] = ''
context['table_label'] = ''

def generate_latex_table(column_names, data, result_path):
    path = result_path + '.txt'
    f = open(path, "w")
    f.write("\\begin{table}\n\\centering\n\\begin{tabular}{ |l|r|r|r| }\n")
    f.write("\\hline\n")
    f.write("Agent & Mean & Median & Standard Deviation\\\\\n")
    f.write("\\hline\n")
    print('Agent, Mean, Median, Standard Deviation')
    for cname in column_names:
        row = data[cname]
        print(cname, "{:.2f}".format(np.mean(row)), "{:.2f}".format(np.median(row)), "{:.2f}".format(np.std(row)))
        f.write(cname + ' & ' + "{:.2f}".format(np.mean(row)) + ' & ' + "{:.2f}".format(np.median(row)) + ' & ' + "{:.2f}".format(np.std(row)) + "\\\\\n")
    f.write("\\hline\n\end{tabular}\\caption{" + context['table_caption'] + "}\n")
    f.write("\\label{" + context['table_label'] + "}\n")
    f.write("\\end{table}")

def draw(data_sources, result_path):
    if os.path.exists(result_path):
        print(result_path + ' already exists. Skip processing data sources')
        return
    
    plt.rcParams["figure.figsize"] = context['figsize']
    data = {}
    column_names = []
    for ds in data_sources:
        file = ds.data_parent_path + '/times.txt'
        if not os.path.exists(file):
            file = ds.data_parent_path + '/learning-times.txt'
        cells = []
        multiplier = 1 if ds.multiplier == None else ds.multiplier 
        with open(file, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=' ')
            for row in plots:
                if context['use_ltpe']:
                    t = float(row[4]) / ds.num_episodes
                else:
                    t = float(row[4]) * multiplier / 3600
                cells.append(t)
        data[ds.name] = cells
        column_names.append(ds.name)
    dataframe = pd.DataFrame(data, columns=column_names)

    plt.rcParams["figure.figsize"] = context['figsize']
    x_1 = np.arange(1, 2)
    distance_btw_agents = context['distance_btw_agents']
    colors = context['palette']
    for index, label in enumerate(column_names):
        y = []
        errors = []
        agent_data = data[label]
        mean, error = ScipyBootstrap().execute_with_errors(agent_data, 10000, 'bca')
        y.append(mean)
        errors.append(error)
        errors = np.array(errors).T
        y = np.array(y)
        plt.errorbar(x=x_1, y=y, yerr=errors, color='gray', capsize=3,
            linestyle="None", marker="s", markersize=7, mfc=colors[index], mec="black", label=label)
        x_1 = x_1 + distance_btw_agents

    plt.ylabel(context['ylabel'], fontsize=11)
    # if 'ylim' in context:
    #     plt.ylim(context['ylim'])
    if 'legend_loc' in context:
        plt.legend(loc=context['legend_loc'], ncol=context['legend_num_columns'])
    else:
        plt.legend(loc='upper center', ncol=context['legend_num_columns'])
    plt.grid(axis='y')
    plt.xticks([])  
    plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced 
    if result_path is not None:
        plt.savefig(result_path)     
    plt.show()
    return
    generate_latex_table(column_names, data, result_path)

if __name__ == '__main__':
    p = 'ace-zero-rl/revised_thesis/'
    context['show_figures'] = True
    parent = p + '../rl2020_results/'
    parent_mo = p + '../rl2021_mo_results/'

    """ DQN and PPO """    
    context['table_caption'] = "DQN, DQN-wTN, double DQN and PPO learning times"
    context['table_label'] = "tbl:dqn-learning-times"
    result_path = p + './learning_times/dqn_ppo_learning_times_errorbars.pdf'
    colors = ['#f8f8f8', '#e8e8e8', '#d7d7d7', '#f8f8f8', '#e8e8e8', '#909090', 
              'LightGreen', 'MediumSpringGreen', 'GreenYellow', 'Green', 'darkGreen', 'darkGreen',
              'LightBlue', 'MediumBlue', 'SkyBlue', 'Blue', 'darkBlue', 'darkBlue',
              'red', 'red', 'red', 'red', 'red', 'orange']
    colors = sns.color_palette('hls', 24).as_hex()
    context['palette'] = colors
    context['figsize'] = (8, 6)
    context['ylabel'] = 'Total Learning Time (hours)'
    context['legend_num_columns'] = 2
    context['legend_loc'] = 'lower left'
    data_sources = [
            DataSource(name='dqn-001-20K', data_parent_path=parent + 'dqn-so/dqn-001', num_episodes=20_000),
            DataSource(name='dqn-002-20K', data_parent_path=parent + 'dqn-so/dqn-002', num_episodes=20_000),
            DataSource(name='dqn-003-20K', data_parent_path=parent + 'dqn-so/dqn-003', num_episodes=20_000),
            DataSource(name='dqn-004-20K', data_parent_path=parent + 'dqn-so/dqn-004', num_episodes=20_000),
            DataSource(name='dqn-005-20K', data_parent_path=parent + 'dqn-so/dqn-005', num_episodes=20_000),
            DataSource(name='dqn-random-20K', data_parent_path=parent + 'dqn-so/dqn-random', num_episodes=20_000),
            DataSource(name='dqn-wtn-001-20K', data_parent_path=parent + 'dqn-wtn-so/dqn-wtn-c700-001', num_episodes=20_000),
            DataSource(name='dqn-wtn-002-20K', data_parent_path=parent + 'dqn-wtn-so/dqn-wtn-c700-002', num_episodes=20_000),
            DataSource(name='dqn-wtn-003-20K', data_parent_path=parent + 'dqn-wtn-so/dqn-wtn-c700-003', num_episodes=20_000),
            DataSource(name='dqn-wtn-004-20K', data_parent_path=parent + 'dqn-wtn-so/dqn-wtn-c700-004', num_episodes=20_000),
            DataSource(name='dqn-wtn-005-20K', data_parent_path=parent + 'dqn-wtn-so/dqn-wtn-c700-005', num_episodes=20_000),
            DataSource(name='dqn-wtn-random-20K', data_parent_path=parent + 'dqn-wtn-so/dqn-wtn-c700-random', num_episodes=20_000),
            DataSource(name='ddqn-001-20K', data_parent_path=parent + 'double-dqn-so/double-dqn-001', num_episodes=20_000),
            DataSource(name='ddqn-002-20K', data_parent_path=parent + 'double-dqn-so/double-dqn-002', num_episodes=20_000),
            DataSource(name='ddqn-003-20K', data_parent_path=parent + 'double-dqn-so/double-dqn-003', num_episodes=20_000),
            DataSource(name='ddqn-004-20K', data_parent_path=parent + 'double-dqn-so/double-dqn-004', num_episodes=20_000),
            DataSource(name='ddqn-005-20K', data_parent_path=parent + 'double-dqn-so/double-dqn-005', num_episodes=20_000),
            DataSource(name='ddqn-random-20K', data_parent_path=parent + 'double-dqn-so/double-dqn-random', num_episodes=20_000),
            DataSource(name='ppo-001-20K', data_parent_path=parent + 'ppo-so/ppo4K-001', num_episodes=20_000),
            DataSource(name='ppo-002-20K', data_parent_path=parent + 'ppo-so/ppo4K-002', num_episodes=20_000),
            DataSource(name='ppo-003-20K', data_parent_path=parent + 'ppo-so/ppo4K-003', num_episodes=20_000),
            DataSource(name='ppo-004-20K', data_parent_path=parent + 'ppo-so/ppo4K-004', num_episodes=20_000),
            DataSource(name='ppo-005-20K', data_parent_path=parent + 'ppo-so/ppo4K-005', num_episodes=20_000),
            DataSource(name='ppo-random-20K', data_parent_path=parent + 'ppo-so/ppo4K-random', num_episodes=20_000)
        ]
    draw(data_sources, result_path)
    
    
    context['table_caption'] = "DQN, DQN-wTN and double DQN learning times per episode"
    context['table_label'] = "tbl:dqn-learning-times-per-episode"
    context['use_ltpe'] = True
    context['ylabel'] = 'Learning Time/Episode (seconds)'
    result_path = p + './learning_times/dqn_ppo_learning_times_per_episode_errorbars.pdf'
    draw(data_sources, result_path)


    
    
    """ Q-lambda and actor-critic only"""
    context['use_ltpe'] = False
    context['figsize'] = (5, 4)
    context['legend_loc'] = 'upper left'
    context['legend_num_columns'] = 1
    colors = sns.color_palette('hls', 12).as_hex()
    context['palette'] = colors
    result_path = p + './learning_times/ql_ac_learning_times_errorbars.pdf'
    context['ylabel'] = 'Total Learning Time (hours)'
    data_sources = [
            DataSource(name='ql-001-200K', data_parent_path=parent + 'ql-so-200K/ql-001', num_episodes=200_000),
            DataSource(name='ql-002-200K', data_parent_path=parent + 'ql-so-200K/ql-002', num_episodes=200_000),
            DataSource(name='ql-003-200K', data_parent_path=parent + 'ql-so-200K/ql-003', num_episodes=200_000),
            DataSource(name='ql-004-200K', data_parent_path=parent + 'ql-so-200K/ql-004', num_episodes=200_000),
            DataSource(name='ql-005-200K', data_parent_path=parent + 'ql-so-200K/ql-005', num_episodes=200_000),
            DataSource(name='ql-random-200K', data_parent_path=parent + 'ql-so-200K/ql-random', num_episodes=200_000),
            DataSource(name='ac-001-200K', data_parent_path=parent + 'ac-so/ac-001', num_episodes=100_000, multiplier=2),
            DataSource(name='ac-002-200K', data_parent_path=parent + 'ac-so/ac-002', num_episodes=100_000, multiplier=2),
            DataSource(name='ac-003-200K', data_parent_path=parent + 'ac-so-500K/ac-003', num_episodes=200_000, multiplier=1),
            DataSource(name='ac-004-200K', data_parent_path=parent + 'ac-so-500K/ac-004', num_episodes=200_000, multiplier=1),
            DataSource(name='ac-005-200K', data_parent_path=parent + 'ac-so-500K/ac-005', num_episodes=200_000, multiplier=1),
            DataSource(name='ac-random-200K', data_parent_path=parent + 'ac-so-500K/ac-random', num_episodes=500_000, multiplier=0.4),
        ]
    draw(data_sources, result_path)
    
    context['table_caption'] = "Learning times in hours"
    context['table_label'] = "tbl:ql-ac-learning-times"
    context['use_ltpe'] = True
    context['ylabel'] = 'Learning Time/Episode (seconds)'
    result_path = p + './learning_times/ql_ac_learning_times_per_episode_errorbars.pdf'
    draw(data_sources, result_path)

    ''' MORL only'''
    context['use_ltpe'] = False
    context['table_caption'] = "Learning times in hours for generating policies"
    context['table_label'] = "tbl:learning-times-various-policies"
    context['figsize'] = (5, 4)
    result_path = p + './learning_times/mo_rb001_rb003_learning_times_errorbars.pdf'
    context['ylabel'] = 'Total Learning Time (hours)'
    data_sources = [
        DataSource(name='mo-ql-random-200K-RB001', data_parent_path=parent_mo + 'ql-mo/ql-mo-001-200000-rb001', num_episodes=200_000),
        DataSource(name='mo-ql-random-200K-RB002', data_parent_path=parent_mo + 'ql-mo/ql-mo-random-200000-rb002', num_episodes=200_000),
        DataSource(name='mo-ql-random-200K-RB003', data_parent_path=parent_mo + 'ql-mo/ql-mo-random-200000-rb003', num_episodes=200_000),
        DataSource(name='mo-ac-random-200K-RB001', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-200000-rb004', num_episodes=200_000),
        DataSource(name='mo-ac-random-200K-RB002', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-200000-rb002', num_episodes=200_000),
        DataSource(name='mo-ac-random-200K-RB003', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-200000-rb003', num_episodes=200_000),
        DataSource(name='mo-dqn-shared-random-20K-RB001', data_parent_path=parent_mo + 'dqn-mo-shared/dqn-mo-shared-random-20000-rb001', num_episodes=20_000),
        DataSource(name='mo-dqn-shared-random-20K-RB002', data_parent_path=parent_mo + 'dqn-mo-shared/dqn-mo-shared-random-20000-rb002', num_episodes=20_000),
        DataSource(name='mo-dqn-shared-random-20K-RB003', data_parent_path=parent_mo + 'dqn-mo-shared/dqn-mo-shared-random-20000-rb003', num_episodes=20_000),
        DataSource(name='mo-dqn-mnn-random-20K-RB001', data_parent_path=parent_mo + 'dqn-mo-mnn/dqn-mo-mnn-random-20000-rb001', num_episodes=20_000),
        DataSource(name='mo-dqn-mnn-random-20K-RB002', data_parent_path=parent_mo + 'dqn-mo-mnn/dqn-mo-mnn-random-20000-rb002', num_episodes=20_000),
        DataSource(name='mo-dqn-mnn-random-20K-RB003', data_parent_path=parent_mo + 'dqn-mo-mnn/dqn-mo-mnn-random-20000-rb003', num_episodes=20_000),
    ]
    draw(data_sources, result_path)
    
    context['table_caption'] = "Learning times in hours for generating policies"
    context['table_label'] = "tbl:learning-times-various-policies"
    context['use_ltpe'] = True
    context['ylabel'] = 'Learning Time/Episode (seconds)'
    result_path = p + './learning_times/mo_rb001_rb003_learning_times_per_episode_errorbars.pdf'
    draw(data_sources, result_path)
    
        
    context['use_ltpe'] = False
    context['table_caption'] = "Learning times in hours for generating policies"
    context['table_label'] = "tbl:learning-times-various-policies"
    colors = ['LightCyan', 'LightSkyBlue', 'MediumBlue', 'lightCyan', 'lightSkyBlue', 'darksalmon', 
              '#f8f8f8', '#e8e8e8', '#d7d7d7', '#f8f8f8', '#e8e8e8', '#909090',
              'red', 'red', 'red', 'red',
              'LightGreen', 'MediumSpringGreen', 'GreenYellow', 'Green'] 
    context['palette'] = colors
    context['figsize'] = (3.5, 4)
    context['legend_loc'] = 'lower right'

    result_path = p + './learning_times/mo_rb004_rb007_learning_times_errorbars.pdf'
    context['ylabel'] = 'Total Learning Time (hours)'
    data_sources = [
        DataSource(name='mo-ac-random-200K-RB004', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb013', num_episodes=500_000, multiplier=0.4),
        DataSource(name='mo-ac-random-200K-RB005', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb014', num_episodes=500_000, multiplier=0.4),
        DataSource(name='mo-ac-random-200K-RB006', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb015', num_episodes=500_000, multiplier=0.4),
        DataSource(name='mo-ac-random-200K-RB007', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb016', num_episodes=500_000, multiplier=0.4),
    ]
    draw(data_sources, result_path)
    
    #context['figsize'] = (12, 8)
    context['table_caption'] = "Learning times in hours for generating policies"
    context['table_label'] = "tbl:learning-times-various-policies"
    context['use_ltpe'] = True
    context['ylabel'] = 'Learning Time/Episode (seconds)'
    result_path = p + './learning_times/mo_rb004_rb007_learning_times_per_episode_errorbars.pdf'
    draw(data_sources, result_path)
    

    """ all methods """
    context['use_ltpe'] = False
    context['table_caption'] = "Learning times in hours for generating policies"
    context['table_label'] = "tbl:learning-times-various-policies"
    colors = ['LightCyan', 'LightSkyBlue', 'MediumBlue', 'lightCyan', 'lightSkyBlue', 'darksalmon', 
              '#f8f8f8', '#e8e8e8', '#d7d7d7', '#f8f8f8', '#e8e8e8', '#909090',
              'red', 'red', 'red', 'red',
              'LightGreen', 'MediumSpringGreen', 'GreenYellow', 'Green']
    context['palette'] = colors
    context['figsize'] = (8, 5)
    context['legend_num_columns'] = 2
    result_path = p + './learning_times/all_approaches_learning_times_errorbars.pdf'
    context['ylabel'] = 'Total Learning Time (hours)'
    context['legend_loc'] = 'lower left'
    data_sources = [
            DataSource(name='ac-001-200K', data_parent_path=parent + 'ac-so/ac-001', num_episodes=100_000, multiplier=2),
            DataSource(name='ac-002-200K', data_parent_path=parent + 'ac-so/ac-002', num_episodes=100_000, multiplier=2),
            DataSource(name='ac-003-200K', data_parent_path=parent + 'ac-so-500K/ac-003', num_episodes=200_000, multiplier=1),
            DataSource(name='ac-004-200K', data_parent_path=parent + 'ac-so-500K/ac-004', num_episodes=200_000, multiplier=1),
            DataSource(name='ac-005-200K', data_parent_path=parent + 'ac-so-500K/ac-005', num_episodes=200_000, multiplier=1),
            DataSource(name='ac-random-200K', data_parent_path=parent + 'ac-so-500K/ac-random', num_episodes=500_000, multiplier=0.4),
            
            DataSource(name='dqn-001-20K', data_parent_path=parent + 'dqn-so/dqn-001', num_episodes=20_000),
            DataSource(name='dqn-002-20K', data_parent_path=parent + 'dqn-so/dqn-002', num_episodes=20_000),
            DataSource(name='dqn-003-20K', data_parent_path=parent + 'dqn-so/dqn-003', num_episodes=20_000),
            DataSource(name='dqn-004-20K', data_parent_path=parent + 'dqn-so/dqn-004', num_episodes=20_000),
            DataSource(name='dqn-005-20K', data_parent_path=parent + 'dqn-so/dqn-005', num_episodes=20_000),
            DataSource(name='dqn-random-20K', data_parent_path=parent + 'dqn-so/dqn-random', num_episodes=20_000),

            DataSource(name='d2dspl', data_parent_path=p + './d2d-learning-time-data/d2dspl', num_episodes=200_000),
            DataSource(name='d2dsql-random-11K', data_parent_path=p + './d2d-learning-time-data/d2dsql-11k', num_episodes=200_000),
            DataSource(name='d2dsql-random-12K', data_parent_path=p + './d2d-learning-time-data/d2dsql-12k', num_episodes=200_000),
            DataSource(name='d2dsql-random-13K', data_parent_path=p + './d2d-learning-time-data/d2dsql-13k', num_episodes=200_000),
            
            DataSource(name='mo-ac-random-200K-RB004', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb013', num_episodes=500_000, multiplier=0.4),
            DataSource(name='mo-ac-random-200K-RB005', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb014', num_episodes=500_000, multiplier=0.4),
            DataSource(name='mo-ac-random-200K-RB006', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb015', num_episodes=500_000, multiplier=0.4),
            DataSource(name='mo-ac-random-200K-RB007', data_parent_path=parent_mo + 'ac-mo/ac-mo-random-500000-rb016', num_episodes=500_000, multiplier=0.4),
        ]
    # draw(data_sources, result_path)
    
    #context['figsize'] = (12, 8)
    context['legend_loc'] = 'center'
    context['table_caption'] = "Learning times in hours for generating policies"
    context['table_label'] = "tbl:learning-times-various-policies"
    context['use_ltpe'] = True
    context['ylabel'] = 'Learning Time/Episode (seconds)'
    result_path = p + './learning_times/all_approaches_learning_times_per_episode_errorbars.pdf'
    draw(data_sources, result_path)
    
