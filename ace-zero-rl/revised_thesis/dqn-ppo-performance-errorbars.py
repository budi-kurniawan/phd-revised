from util import *
import os
os.system('cls' if os.name == 'nt' else 'clear')
# gradient color codes: http://www.perbang.dk/rgb/00BABF/
if __name__ == '__main__':
    p = 'ace-zero-rl/revised_thesis/'
    # use this go get color list: sns.color_palette('PRGn').as_hex()
    colors = ['#844793', '#bc9eca', '#ebdeec', '#e1f2dd', '#9cd597', '#358e48']
    context['palette'] = colors
    context['figsize'] = (6.5, 3.8)

    parent = p + '../rl2020_test_results/dqn-so/'
    parent_ppo = p + '../rl2020_test_results/ppo-so/'
    parent_mo_shared = p + '../rl2020_test_results/dqn-mo-shared/'
    parent_baseline = p + '../rl2020_test_results/baseline/'
    context['baseline_color'] = 'red'
    context['ylim'] = (0, .55)
    # result_path = p + './dqn-performance/dqn-mo-performance-boxplot.pdf'
    # data_sources = [
    #         BehaviourDataSource(label='dqn-mo-shared-random-20K', data_parent_path=parent_mo_shared + 
    #                             'dqn-mo-shared-random-20000-rb001-basic-a', num_trials=10),
    #         BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
    #     ]
    # draw_error_bars(data_sources, result_path)

    result_path = p + './dqn-performance/dqn-performance-errorbars.pdf'
    data_sources = [
            BehaviourDataSource(label='dqn-001', data_parent_path=parent + 'dqn-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-002', data_parent_path=parent + 'dqn-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-003', data_parent_path=parent + 'dqn-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-004', data_parent_path=parent + 'dqn-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-005', data_parent_path=parent + 'dqn-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-random', data_parent_path=parent + 'dqn-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw_error_bars(data_sources, result_path)
        
    result_path = p + './dqn-performance/dqn-wtn-c700-performance-errorbars.pdf'
    data_sources = [
            BehaviourDataSource(label='dqn-wtn-c700-001', data_parent_path=parent + 'dqn-wtn-c700-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-002', data_parent_path=parent + 'dqn-wtn-c700-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-003', data_parent_path=parent + 'dqn-wtn-c700-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-004', data_parent_path=parent + 'dqn-wtn-c700-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-005', data_parent_path=parent + 'dqn-wtn-c700-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-random', data_parent_path=parent + 'dqn-wtn-c700-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw_error_bars(data_sources, result_path)
    
    result_path = p + './dqn-performance/double-dqn-performance-errorbars.pdf'
    data_sources = [
            BehaviourDataSource(label='double-dqn-001', data_parent_path=parent + 'double-dqn-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-002', data_parent_path=parent + 'double-dqn-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-003', data_parent_path=parent + 'double-dqn-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-004', data_parent_path=parent + 'double-dqn-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-005', data_parent_path=parent + 'double-dqn-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-random', data_parent_path=parent + 'double-dqn-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]    
    draw_error_bars(data_sources, result_path)
    
    result_path = p + './ppo-performance/ppo-performance-errorbars.pdf'
    context['ylim'] = (0, .03)
    context['figsize'] = (6.5, 3.8)
    data_sources = [
            BehaviourDataSource(label='ppo-001', data_parent_path=parent_ppo + 'ppo4K-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-002', data_parent_path=parent_ppo + 'ppo4K-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-003', data_parent_path=parent_ppo + 'ppo4K-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-004', data_parent_path=parent_ppo + 'ppo4K-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-005', data_parent_path=parent_ppo + 'ppo4K-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-random', data_parent_path=parent_ppo + 'ppo4K-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw_error_bars(data_sources, result_path)
    