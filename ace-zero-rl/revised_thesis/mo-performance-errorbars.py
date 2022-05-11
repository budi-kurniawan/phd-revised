from util import *
import seaborn as sns
import os
os.system('cls' if os.name == 'nt' else 'clear')
# gradient color codes: http://www.perbang.dk/rgb/00BABF/
if __name__ == '__main__':
    p = 'ace-zero-rl/revised_thesis/'
    parent = p + '../rl2020_test_results/dqn-so/'
    parent_ac_mo = p + '../rl2020_test_results/ac-mo/'
    parent_ql_mo = p + '../rl2020_test_results/ql-mo/'
    parent_dqn_mo_shared = p + '../rl2020_test_results/dqn-mo-shared/'
    parent_dqn_momnn = p + '../rl2020_test_results/dqn-mo-mnn/'
    parent_baseline = p + '../rl2020_test_results/baseline/'
    # context['palette'] = 'PRGn' # 'cubehelix' #'husl', 'coolwarm', 'Blues', 'Reds', 'Greens' etc
    context['baseline_color'] = 'red'
    
    colors = ['#efffef', '#ccffe0', '#b2ffd0', '#99ffc1', '#00ff64', '#fff9b2', 'orange',
            '#efffef', '#ccffe0', '#b2ffd0', '#99ffc1', '#00ff64', '#fff9b2', 'orange',
        ] #https://www.w3schools.com/colors/colors_gradient.asp
    colors = sns.color_palette('PRGn', 12).as_hex()
    context['palette'] = colors
    context['figsize'] = (8, 5.5)
    context['distance_btw_agents'] = 0.07
    """ rb001-rb006, all agents """
    context['ylim'] = (0, .4)
    # context['legend_loc'] = (0.3, 0.4)
    result_path = p + './mo-performance/rb001-rb003_all_agents_performance.pdf'
    data_sources = [
            BehaviourDataSource(label='mo-ql-random-200K-RB001', data_parent_path=parent_ql_mo + 
                                'ql-mo-001-200000-rb001-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-ql-random-200K-RB002', data_parent_path=parent_ql_mo + 
                                'ql-mo-random-200000-rb002-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-ql-random-200K-RB003', data_parent_path=parent_ql_mo + 
                                'ql-mo-random-200000-rb003-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-ac-random-200K-RB001', data_parent_path=parent_ac_mo + 
                                'ac-mo-001-200000-rb001-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-ac-random-200K-RB002', data_parent_path=parent_ac_mo + 
                                'ac-mo-random-200000-rb002-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-ac-random-200K-RB003', data_parent_path=parent_ac_mo + 
                                'ac-mo-random-200000-rb003-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-dqn-shared-random-20K-RB001', data_parent_path=parent_dqn_mo_shared + 
                                'dqn-mo-shared-random-20000-rb001-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-dqn-shared-random-20K-RB002', data_parent_path=parent_dqn_mo_shared + 
                                'dqn-mo-shared-random-20000-rb002-basic-a', num_trials=10),
            BehaviourDataSource(label='mo-dqn-shared-random-20K-RB003', data_parent_path=parent_dqn_mo_shared + 
                                'dqn-mo-shared-random-20000-rb003-basic-a', num_trials=10),
            
            BehaviourDataSource(label='mo-dqn-mnn-random-20K-RB001', data_parent_path=parent_dqn_momnn + 
                                'dqn-momnn-random-20000-rb001-basic-a', num_trials=5),
            BehaviourDataSource(label='mo-dqn-mnn-random-20K-RB002', data_parent_path=parent_dqn_momnn + 
                                'dqn-momnn-random-7000-rb002-basic-a', num_trials=5),
            BehaviourDataSource(label='mo-dqn-mnn-random-20K-RB003', data_parent_path=parent_dqn_momnn + 
                                'dqn-momnn-random-7000-rb003-basic-a', num_trials=5),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    # draw_error_bars(data_sources, result_path)


    """ MO ACET """
    context['ylim'] = (0, .55)
    colors = ['coral', 'darksalmon', 'darkkhaki', 'darkorchid', 'cyan', 'greenyellow', 'yellow'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    context['figsize'] = (6.5, 4)
    context['distance_btw_agents'] = 0.09
    parent = p + '../rl2020_test_results/ac-mo/'
    parent_so = p + '../rl2020_test_results/ac-so/'
    parent_baseline = p + '../rl2020_test_results/baseline/'
    result_path = p + './mo-performance/mo-ac-random-rb4-5-6-7-performance-errorbars.pdf'

    """ ac-random-500K and ac-random-1M are the best performers among single objective AC agents"""    
    data_sources = [
            BehaviourDataSource(label='ac-random-200K', data_parent_path=parent_so + 'ac-random-200000-basic-a'),
            BehaviourDataSource(label='mo-ac-random-200K-RB004', data_parent_path=parent + 'ac-mo-random-001-200000-rb013-basic-a'),
            BehaviourDataSource(label='mo-ac-random-200K-RB005', data_parent_path=parent + 'ac-mo-random-001-200000-rb014-basic-a'),
            BehaviourDataSource(label='mo-ac-random-200K-RB006', data_parent_path=parent + 'ac-mo-random-001-200000-rb015-basic-a'),
            BehaviourDataSource(label='mo-ac-random-200K-RB007', data_parent_path=parent + 'ac-mo-random-001-500000-rb016-basic-a'),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw_error_bars(data_sources, result_path)