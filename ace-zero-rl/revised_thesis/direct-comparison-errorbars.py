import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import csv
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import namedtuple
from matplotlib.ticker import FuncFormatter
from util import *
os.system('cls' if os.name == 'nt' else 'clear')

DataSource = namedtuple('DataSource', 'name data_path result_path', defaults=[None, None])
context = {'num_trials': 10, 'max_records': 100_000, 'num_avg_samples': 250, 'offset': 0.5, 
    'show_figures': False, 'ylim': (0, 1), 'label': None,
    'distance_btw_agents': 0.09, 'ylabel': 'Number of wins - number of losses', 'legend_num_columns':1,
    'label_fontsize':11}


def get_data(data_sources):
    data = []
    labels = []
    for data_source in data_sources:
        labels.append(data_source.name)
        for trial in range(context['num_trials']):
            path = data_source.data_path + '/blue-red-scores-0' + str(trial) + '.txt'
            blue_wins = 0
            red_wins = 0
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if row[0].isdigit():
                        episode = (int(row[0]))
                        blue_score = float(row[1])
                        red_score = float(row[2])
                        if blue_score > red_score:
                            blue_wins += 1
                        elif red_score > blue_score:
                            red_wins += 1
                    else:
                        break
            sample = {'value': blue_wins - red_wins, 'name':data_source.name}
            data.append(sample)
    return data, labels

def create_charts(data, labels, result_path):
    plt.rcParams["figure.figsize"] = context['figsize']
    x_1 = np.arange(1, 2)
    colors = context['palette']
    distance_btw_agents = context['distance_btw_agents']
    for index, label in enumerate(labels):
        y = []
        errors = []
        agent_data = [x for x in data if x['name']==label]
        values = [x['value'] for x in agent_data]
        mean, error = ScipyBootstrap().execute_with_errors(values, 10000, 'bca')
        y.append(mean)
        errors.append(error)
        errors = np.array(errors).T
        y = np.array(y)
        plt.errorbar(x=x_1, y=y, yerr=errors, color='gray', capsize=3,
            linestyle="None", marker="s", markersize=7, mfc=colors[index], mec="black", label=label)
        x_1 = x_1 + distance_btw_agents

    plt.ylabel(context['ylabel'], fontsize=context['label_fontsize'])
    if 'ylim' in context:
        plt.ylim(context['ylim'])
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

def create_latex_tables(data, path):
    columns = {}
    for row in data:
        name = row['name']
        value = row['value']
        if name not in columns:
            columns[name] = []
        columns[name].append(value)
    column_names = []
    rows = []
    for k, v in columns.items():
        column_names.append(k)
        rows.append(v)
        #print(k, v)
    rows = np.array(rows).transpose()
    trial = 0
    f = open(path, 'w')
    f.write('\\begin{table}[H]' + '\n')
    f.write('\\centering' + '\n')
    s = '|c' + '|r' * (len(column_names)) + '|'
    print(s)
    f.write('\\begin{tabular}{' + s + ' } ' + '\n')
    f.write('\\hline' + '\n')

    s = ' & ' + ' & '.join(column_names) + '\\\\'
    print(s)
    f.write(s + '\n')
    f.write('\\hline' + '\n')
    for row in rows:
        s = 'Trial ' + str(trial) + ' & ' + np.array2string(row, separator=' & ', max_line_width=np.inf)[1:-1] + '\\\\'
        trial += 1
        f.write(s + '\n')
        print(s)
    medians = np.median(rows, axis=0)
    s = 'Median & ' + np.array2string(medians, separator=' & ', max_line_width=np.inf, 
            formatter={'float_kind':lambda x: "%.2f" % x})[1:-1] + '\\\\'
    print(s)
    f.write('\\hline' + '\n')
    f.write(s + '\n')
    f.write('\\hline' + '\n')
    f.write('\\end{tabular}' + '\n')
    f.write('\\caption{' + path + '}\n')
    f.write('\\label{}\n')
    f.write('\\end{table}\n')

    f.close()

def process(data_sources, path):
    # if os.path.exists(path + '.pdf'):
    #     print(path + '.pdf already exists. Skip processing data sources')
    #     return
    data, labels = get_data(data_sources)
    create_charts(data, labels, path + '.pdf')
    #create_latex_tables(data, path + '-latex-table.txt')
    
if __name__ == "__main__":
    p = 'ace-zero-rl/revised_thesis/'
    parent = p + '../rl2020_test_results/'
    parent_dqn = p + '../rl2020_test_results/dqn-so/'
    parent_ac_so = p + '../rl2020_test_results/ac-so/'
    parent_ac_mo = p + '../rl2020_test_results/ac-mo/'
    parent_d2dsql = p + '../rl2020_test_results/d2dsql2/direct-comparison/'
    result_parent = p + './direct-comparisons'
    if not os.path.exists(result_parent):
        os.mkdir(result_parent)

    context['show_figures'] = False
    context['figsize'] = (10, 3)
    context['legend_num_columns'] = 4
    context['legend_loc'] = 'upper center'
    context['ylim'] = (-150, 230)
    context['max_records'] = 1000_000
    context['num_trials'] = 10
    context['num_avg_samples'] = 250
    context['offset'] = 0
    context['show_figures'] = True
    colors = sns.color_palette('YlOrBr', 12).as_hex()[0:6]
    colors = colors + sns.color_palette('Blues', 12).as_hex()[0:6]
    colors = colors + sns.color_palette('Spectral', 6).as_hex()[0:3]
    colors = colors + sns.color_palette('Greens', 6).as_hex()[0:4]
    context['palette'] = colors

    data_sources = [
#             DataSource(name='ac-001-100k', data_path=parent + 'ac-001-100000-red-pure-pursuit-basic-a'),
#             DataSource(name='ac-002-100k', data_path=parent + 'ac-002-100000-red-pure-pursuit-basic-a'),
#             DataSource(name='ac-003-100k', data_path=parent + 'ac-003-100000-red-pure-pursuit-basic-a'),
#             DataSource(name='ac-004-100k', data_path=parent + 'ac-004-100000-red-pure-pursuit-basic-a'),
#             DataSource(name='ac-005-100k', data_path=parent + 'ac-005-100000-red-pure-pursuit-basic-a'),
#             DataSource(name='ac-random-500k', data_path=parent + 'ac-random-500000-red-pure-pursuit-basic-a'),
            DataSource(name='ac-001-200k', data_path=parent_ac_so + 'ac-001-200000-red-pure-pursuit-basic-a'),
            DataSource(name='ac-002-200k', data_path=parent_ac_so + 'ac-002-200000-red-pure-pursuit-basic-a'),
            DataSource(name='ac-003-200k', data_path=parent_ac_so + 'ac-003-200000-red-pure-pursuit-basic-a'),
            DataSource(name='ac-004-200k', data_path=parent_ac_so + 'ac-004-200000-red-pure-pursuit-basic-a'),
            DataSource(name='ac-005-200k', data_path=parent_ac_so + 'ac-005-200000-red-pure-pursuit-basic-a'),
            DataSource(name='ac-random-200k', data_path=parent_ac_so + 'ac-random-200000-red-pure-pursuit-basic-a'),

            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-red-pure-pursuit-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-red-pure-pursuit-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-red-pure-pursuit-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-red-pure-pursuit-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-red-pure-pursuit-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-red-pure-pursuit-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-red-pure-pursuit-basic-a'),

            DataSource(name='d2dsql-random-11k', data_path=parent_d2dsql + 'd2dsql2-random-11000-red-pure-pursuit-basic-a'),
            DataSource(name='d2dsql-random-12k', data_path=parent_d2dsql + 'd2dsql2-random-12000-red-pure-pursuit-basic-a'),
            DataSource(name='d2dsql-random-13k', data_path=parent_d2dsql + 'd2dsql2-random-13000-red-pure-pursuit-basic-a'),

            DataSource(name='mo-ac-200k-RB004', data_path=parent_ac_mo + 'ac-mo-random-500000-rb013-red-pure-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB005', data_path=parent_ac_mo + 'ac-mo-random-500000-rb014-red-pure-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB006', data_path=parent_ac_mo + 'ac-mo-random-500000-rb015-red-pure-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB007', data_path=parent_ac_mo + 'ac-mo-random-500000-rb016-red-pure-pursuit-basic-a')
    ]
    # process(data_sources, result_parent + '/vs-pure-pursuit-agent')
    # sys.exit()

    data_sources = [
#             DataSource(name='ac-001-100k', data_path=parent + 'ac-001-100000-red-smart-pursuit-basic-a'),
#             DataSource(name='ac-002-100k', data_path=parent + 'ac-002-100000-red-smart-pursuit-basic-a'),
#             DataSource(name='ac-003-100k', data_path=parent + 'ac-003-100000-red-smart-pursuit-basic-a'),
#             DataSource(name='ac-004-100k', data_path=parent + 'ac-004-100000-red-smart-pursuit-basic-a'),
#             DataSource(name='ac-005-100k', data_path=parent + 'ac-005-100000-red-smart-pursuit-basic-a'),
#             DataSource(name='ac-random-500k', data_path=parent + 'ac-random-500000-red-smart-pursuit-basic-a'),
            #DataSource(name='ac-random-1m', data_path=parent + 'ac-random-1000000-red-smart-pursuit-basic-a'),

            DataSource(name='ac-001-200k', data_path=parent_ac_so + 'ac-001-200000-red-smart-pursuit-basic-a'),
            DataSource(name='ac-002-200k', data_path=parent_ac_so + 'ac-002-200000-red-smart-pursuit-basic-a'),
            DataSource(name='ac-003-200k', data_path=parent_ac_so + 'ac-003-200000-red-smart-pursuit-basic-a'),
            DataSource(name='ac-004-200k', data_path=parent_ac_so + 'ac-004-200000-red-smart-pursuit-basic-a'),
            DataSource(name='ac-005-200k', data_path=parent_ac_so + 'ac-005-200000-red-smart-pursuit-basic-a'),
            DataSource(name='ac-random-200k', data_path=parent_ac_so + 'ac-random-200000-red-smart-pursuit-basic-a'),
            
            
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-red-smart-pursuit-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-red-smart-pursuit-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-red-smart-pursuit-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-red-smart-pursuit-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-red-smart-pursuit-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-red-smart-pursuit-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-red-smart-pursuit-basic-a'),
            
            DataSource(name='d2dsql-random-11k', data_path=parent_d2dsql + 'd2dsql2-random-11000-red-smart-pursuit-basic-a'),
            DataSource(name='d2dsql-random-12k', data_path=parent_d2dsql + 'd2dsql2-random-12000-red-smart-pursuit-basic-a'),
            DataSource(name='d2dsql-random-13k', data_path=parent_d2dsql + 'd2dsql2-random-13000-red-smart-pursuit-basic-a'),
            
            DataSource(name='mo-ac-200k-RB004', data_path=parent_ac_mo + 'ac-mo-random-500000-rb013-red-smart-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB005', data_path=parent_ac_mo + 'ac-mo-random-500000-rb014-red-smart-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB006', data_path=parent_ac_mo + 'ac-mo-random-500000-rb015-red-smart-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB007', data_path=parent_ac_mo + 'ac-mo-random-500000-rb016-red-smart-pursuit-basic-a')
    ]
    #process(data_sources, result_parent + '/vs-smart-pursuit-agent')
    
    data_sources = [
#             DataSource(name='ac-001-100k', data_path=parent + 'ac-001-100000-red-stern-conversion-basic-a'),
#             DataSource(name='ac-002-100k', data_path=parent + 'ac-002-100000-red-stern-conversion-basic-a'),
#             DataSource(name='ac-003-100k', data_path=parent + 'ac-003-100000-red-stern-conversion-basic-a'),
#             DataSource(name='ac-004-100k', data_path=parent + 'ac-004-100000-red-stern-conversion-basic-a'),
#             DataSource(name='ac-005-100k', data_path=parent + 'ac-005-100000-red-stern-conversion-basic-a'),
#             DataSource(name='ac-random-500k', data_path=parent + 'ac-random-500000-red-stern-conversion-basic-a'),
            #DataSource(name='ac-random-1m', data_path=parent + 'ac-random-1000000-red-stern-conversion-basic-a'),
            DataSource(name='ac-001-200k', data_path=parent_ac_so + 'ac-001-200000-red-stern-conversion-basic-a'),
            DataSource(name='ac-002-200k', data_path=parent_ac_so + 'ac-002-200000-red-stern-conversion-basic-a'),
            DataSource(name='ac-003-200k', data_path=parent_ac_so + 'ac-003-200000-red-stern-conversion-basic-a'),
            DataSource(name='ac-004-200k', data_path=parent_ac_so + 'ac-004-200000-red-stern-conversion-basic-a'),
            DataSource(name='ac-005-200k', data_path=parent_ac_so + 'ac-005-200000-red-stern-conversion-basic-a'),
            DataSource(name='ac-random-200k', data_path=parent_ac_so + 'ac-random-200000-red-stern-conversion-basic-a'),            
            
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-red-stern-conversion-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-red-stern-conversion-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-red-stern-conversion-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-red-stern-conversion-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-red-stern-conversion-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-red-stern-conversion-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-red-stern-conversion-basic-a'),
            
            DataSource(name='d2dsql-random-11k', data_path=parent_d2dsql + 'd2dsql2-random-11000-red-stern-conversion-basic-a'),
            DataSource(name='d2dsql-random-12k', data_path=parent_d2dsql + 'd2dsql2-random-12000-red-stern-conversion-basic-a'),
            DataSource(name='d2dsql-random-13k', data_path=parent_d2dsql + 'd2dsql2-random-13000-red-stern-conversion-basic-a'),
            
            DataSource(name='mo-ac-200k-RB004', data_path=parent_ac_mo + 'ac-mo-random-500000-rb013-red-stern-conversion-basic-a'),
            DataSource(name='mo-ac-200k-RB005', data_path=parent_ac_mo + 'ac-mo-random-500000-rb014-red-stern-conversion-basic-a'),
            DataSource(name='mo-ac-200k-RB006', data_path=parent_ac_mo + 'ac-mo-random-500000-rb015-red-stern-conversion-basic-a'),
            DataSource(name='mo-ac-200k-RB007', data_path=parent_ac_mo + 'ac-mo-random-500000-rb016-red-stern-conversion-basic-a')
    ]
    #process(data_sources, result_parent + '/vs-stern-conversion-agent')
    
    data_sources = [
#             DataSource(name='ac-001-100k', data_path=parent + 'ac-001-100000-red-restricted-pure-pursuit-basic-a'),
#             DataSource(name='ac-002-100k', data_path=parent + 'ac-002-100000-red-restricted-pure-pursuit-basic-a'),
#             DataSource(name='ac-003-100k', data_path=parent + 'ac-003-100000-red-restricted-pure-pursuit-basic-a'),
#             DataSource(name='ac-004-100k', data_path=parent + 'ac-004-100000-red-restricted-pure-pursuit-basic-a'),
#             DataSource(name='ac-005-100k', data_path=parent + 'ac-005-100000-red-restricted-pure-pursuit-basic-a'),
#             DataSource(name='ac-random-500k', data_path=parent + 'ac-random-500000-red-restricted-pure-pursuit-basic-a'),
            #DataSource(name='ac-random-1m', data_path=parent + 'ac-random-1000000-red-restricted-pure-pursuit-basic-a'),

            DataSource(name='ac-001-200k', data_path=parent_ac_so + 'ac-001-200000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='ac-002-200k', data_path=parent_ac_so + 'ac-002-200000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='ac-003-200k', data_path=parent_ac_so + 'ac-003-200000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='ac-004-200k', data_path=parent_ac_so + 'ac-004-200000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='ac-005-200k', data_path=parent_ac_so + 'ac-005-200000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='ac-random-200k', data_path=parent_ac_so + 'ac-random-200000-red-restricted-pure-pursuit-basic-a'),            
            
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-red-restricted-pure-pursuit-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-red-restricted-pure-pursuit-basic-a'),

            DataSource(name='d2dsql-random-11k', data_path=parent_d2dsql + 'd2dsql2-random-11000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='d2dsql-random-12k', data_path=parent_d2dsql + 'd2dsql2-random-12000-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='d2dsql-random-13k', data_path=parent_d2dsql + 'd2dsql2-random-13000-red-restricted-pure-pursuit-basic-a'),
            
            DataSource(name='mo-ac-200k-RB004', data_path=parent_ac_mo + 'ac-mo-random-500000-rb013-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB005', data_path=parent_ac_mo + 'ac-mo-random-500000-rb014-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB006', data_path=parent_ac_mo + 'ac-mo-random-500000-rb015-red-restricted-pure-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB007', data_path=parent_ac_mo + 'ac-mo-random-500000-rb016-red-restricted-pure-pursuit-basic-a')
    ]
    #process(data_sources, result_parent + '/vs-restricted-pure-pursuit-agent')
    
    data_sources = [
#             DataSource(name='ac-001-100k', data_path=parent + 'ac-001-100000-red-restricted-smart-pursuit-basic-a'),
#             DataSource(name='ac-002-100k', data_path=parent + 'ac-002-100000-red-restricted-smart-pursuit-basic-a'),
#             DataSource(name='ac-003-100k', data_path=parent + 'ac-003-100000-red-restricted-smart-pursuit-basic-a'),
#             DataSource(name='ac-004-100k', data_path=parent + 'ac-004-100000-red-restricted-smart-pursuit-basic-a'),
#             DataSource(name='ac-005-100k', data_path=parent + 'ac-005-100000-red-restricted-smart-pursuit-basic-a'),
#             DataSource(name='ac-random-500k', data_path=parent + 'ac-random-500000-red-restricted-smart-pursuit-basic-a'),
            #DataSource(name='ac-random-1m', data_path=parent + 'ac-random-1000000-red-restricted-smart-pursuit-basic-a'),

            DataSource(name='ac-001-200k', data_path=parent_ac_so + 'ac-001-200000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='ac-002-200k', data_path=parent_ac_so + 'ac-002-200000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='ac-003-200k', data_path=parent_ac_so + 'ac-003-200000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='ac-004-200k', data_path=parent_ac_so + 'ac-004-200000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='ac-005-200k', data_path=parent_ac_so + 'ac-005-200000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='ac-random-200k', data_path=parent_ac_so + 'ac-random-200000-red-restricted-smart-pursuit-basic-a'),            
            
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-red-restricted-smart-pursuit-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-red-restricted-smart-pursuit-basic-a'),

            DataSource(name='d2dsql-random-11k', data_path=parent_d2dsql + 'd2dsql2-random-11000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='d2dsql-random-12k', data_path=parent_d2dsql + 'd2dsql2-random-12000-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='d2dsql-random-13k', data_path=parent_d2dsql + 'd2dsql2-random-13000-red-restricted-smart-pursuit-basic-a'),
            
            DataSource(name='mo-ac-200k-RB004', data_path=parent_ac_mo + 'ac-mo-random-500000-rb013-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB005', data_path=parent_ac_mo + 'ac-mo-random-500000-rb014-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB006', data_path=parent_ac_mo + 'ac-mo-random-500000-rb015-red-restricted-smart-pursuit-basic-a'),
            DataSource(name='mo-ac-200k-RB007', data_path=parent_ac_mo + 'ac-mo-random-500000-rb016-red-restricted-smart-pursuit-basic-a')
    ]
    # process(data_sources, result_parent + '/vs-restricted-smart-pursuit-agent')
    
    data_sources = [
#             DataSource(name='ac-001-100k', data_path=parent + 'ac-001-100000-red-restricted-stern-conversion-basic-a'),
#             DataSource(name='ac-002-100k', data_path=parent + 'ac-002-100000-red-restricted-stern-conversion-basic-a'),
#             DataSource(name='ac-003-100k', data_path=parent + 'ac-003-100000-red-restricted-stern-conversion-basic-a'),
#             DataSource(name='ac-004-100k', data_path=parent + 'ac-004-100000-red-restricted-stern-conversion-basic-a'),
#             DataSource(name='ac-005-100k', data_path=parent + 'ac-005-100000-red-restricted-stern-conversion-basic-a'),
#             DataSource(name='ac-random-500k', data_path=parent + 'ac-random-500000-red-restricted-stern-conversion-basic-a'),
            #DataSource(name='ac-random-1m', data_path=parent + 'ac-random-1000000-red-restricted-stern-conversion-basic-a'),

            DataSource(name='ac-001-200k', data_path=parent_ac_so + 'ac-001-200000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='ac-002-200k', data_path=parent_ac_so + 'ac-002-200000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='ac-003-200k', data_path=parent_ac_so + 'ac-003-200000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='ac-004-200k', data_path=parent_ac_so + 'ac-004-200000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='ac-005-200k', data_path=parent_ac_so + 'ac-005-200000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='ac-random-200k', data_path=parent_ac_so + 'ac-random-200000-red-restricted-stern-conversion-basic-a'),            
            
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-red-restricted-stern-conversion-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-red-restricted-stern-conversion-basic-a'),

            DataSource(name='d2dsql-random-11k', data_path=parent_d2dsql + 'd2dsql2-random-11000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='d2dsql-random-12k', data_path=parent_d2dsql + 'd2dsql2-random-12000-red-restricted-stern-conversion-basic-a'),
            DataSource(name='d2dsql-random-13k', data_path=parent_d2dsql + 'd2dsql2-random-13000-red-restricted-stern-conversion-basic-a'),

            DataSource(name='mo-ac-200k-RB004', data_path=parent_ac_mo + 'ac-mo-random-500000-rb013-red-restricted-stern-conversion-basic-a'),
            DataSource(name='mo-ac-200k-RB005', data_path=parent_ac_mo + 'ac-mo-random-500000-rb014-red-restricted-stern-conversion-basic-a'),
            DataSource(name='mo-ac-200k-RB006', data_path=parent_ac_mo + 'ac-mo-random-500000-rb015-red-restricted-stern-conversion-basic-a'),
            DataSource(name='mo-ac-200k-RB007', data_path=parent_ac_mo + 'ac-mo-random-500000-rb016-red-restricted-stern-conversion-basic-a')
    ]
    # process(data_sources, result_parent + '/vs-restricted-stern-conversion-agent')
    
    
    colors = sns.color_palette('Blues', 12).as_hex()[0:6]
    colors = colors + sns.color_palette('Greens', 6).as_hex()[0:4]
    context['palette'] = colors
    context['figsize'] = (7, 3)
    context['legend_num_columns'] = 2
    context['legend_loc'] = 'upper center'
    context['ylim'] = (-150, 230)
    context['label_fontsize'] = 10

    data_sources = [
#             DataSource(name='ac-mo-500k-rb013', data_path=parent + 'ac-mo-random-500000-rb013-vs-ac-random-500000-basic-a'),
#             DataSource(name='ac-mo-500k-rb014', data_path=parent + 'ac-mo-random-500000-rb014-vs-ac-random-500000-basic-a'),
#             DataSource(name='ac-mo-500k-rb015', data_path=parent + 'ac-mo-random-500000-rb015-vs-ac-random-500000-basic-a'),
#             DataSource(name='ac-mo-500k-rb016', data_path=parent + 'ac-mo-random-500000-rb016-vs-ac-random-500000-basic-a'),
#             DataSource(name='dqn-001-20k', data_path=parent + 'dqn-001-20000-vs-ac-random-500000-basic-a'),
#             DataSource(name='dqn-002-20k', data_path=parent + 'dqn-002-20000-vs-ac-random-500000-basic-a'),
#             DataSource(name='dqn-003-20k', data_path=parent + 'dqn-003-20000-vs-ac-random-500000-basic-a'),
#             DataSource(name='dqn-004-20k', data_path=parent + 'dqn-004-20000-vs-ac-random-500000-basic-a'),
#             DataSource(name='dqn-005-20k', data_path=parent + 'dqn-005-20000-vs-ac-random-500000-basic-a'),
#             DataSource(name='dqn-random-50k', data_path=parent + 'dqn-random-50000-vs-ac-random-500000-basic-a'),
#             DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-vs-ac-random-500000-basic-a'),

            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-vs-ac-random-200000-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-vs-ac-random-200000-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-vs-ac-random-200000-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-vs-ac-random-200000-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-vs-ac-random-200000-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-20000-vs-ac-random-200000-basic-a'),
            DataSource(name='mo-ac-200k-RB004', data_path=parent_ac_mo + 'ac-mo-random-200000-rb013-vs-ac-random-200000-basic-a'),
            DataSource(name='mo-ac-200k-RB005', data_path=parent_ac_mo + 'ac-mo-random-200000-rb014-vs-ac-random-200000-basic-a'),
            DataSource(name='mo-ac-200k-RB006', data_path=parent_ac_mo + 'ac-mo-random-200000-rb015-vs-ac-random-200000-basic-a'),
            DataSource(name='mo-ac-200k-RB007', data_path=parent_ac_mo + 'ac-mo-random-200000-rb016-vs-ac-random-200000-basic-a'),
    ]
    # process(data_sources, result_parent + '/vs-actor-critic-random-200k-agent')
    

    context['figsize'] = (4.5, 2.5)
    context['legend_num_columns'] = 2
    context['legend_loc'] = 'upper center'
    context['ylim'] = (-150, 230)
    data_sources = [
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-vs-ac-mo-random-500000-rb013-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-vs-ac-mo-random-500000-rb013-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-vs-ac-mo-random-500000-rb013-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-vs-ac-mo-random-500000-rb013-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-vs-ac-mo-random-500000-rb013-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-vs-ac-mo-random-500000-rb013-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-vs-ac-mo-random-500000-rb013-basic-a')
    ]
    process(data_sources, result_parent + '/vs-actor-critic-mo-random-200k-rb004-agent')
    
    data_sources = [
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-vs-ac-mo-random-500000-rb014-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-vs-ac-mo-random-500000-rb014-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-vs-ac-mo-random-500000-rb014-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-vs-ac-mo-random-500000-rb014-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-vs-ac-mo-random-500000-rb014-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-vs-ac-mo-random-500000-rb014-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-vs-ac-mo-random-500000-rb014-basic-a')
    ]
    process(data_sources, result_parent + '/vs-actor-critic-mo-random-200k-rb005-agent')
    
        
    data_sources = [
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-vs-ac-mo-random-500000-rb015-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-vs-ac-mo-random-500000-rb015-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-vs-ac-mo-random-500000-rb015-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-vs-ac-mo-random-500000-rb015-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-vs-ac-mo-random-500000-rb015-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-vs-ac-mo-random-500000-rb015-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-vs-ac-mo-random-500000-rb015-basic-a')
    ]
    process(data_sources, result_parent + '/vs-actor-critic-mo-random-200k-rb006-agent')
    
    data_sources = [
            DataSource(name='dqn-001-20k', data_path=parent_dqn + 'dqn-001-20000-vs-ac-mo-random-500000-rb016-basic-a'),
            DataSource(name='dqn-002-20k', data_path=parent_dqn + 'dqn-002-20000-vs-ac-mo-random-500000-rb016-basic-a'),
            DataSource(name='dqn-003-20k', data_path=parent_dqn + 'dqn-003-20000-vs-ac-mo-random-500000-rb016-basic-a'),
            DataSource(name='dqn-004-20k', data_path=parent_dqn + 'dqn-004-20000-vs-ac-mo-random-500000-rb016-basic-a'),
            DataSource(name='dqn-005-20k', data_path=parent_dqn + 'dqn-005-20000-vs-ac-mo-random-500000-rb016-basic-a'),
            DataSource(name='dqn-random-20k', data_path=parent_dqn + 'dqn-random-50000-vs-ac-mo-random-500000-rb016-basic-a'),
            #DataSource(name='dqn-random-100k', data_path=parent + 'dqn-random-100000-vs-ac-mo-random-500000-rb016-basic-a')
    ]
    process(data_sources, result_parent + '/vs-actor-critic-mo-random-200k-rb007-agent')