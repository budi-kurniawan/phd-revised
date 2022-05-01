from rl2020_graph_generator.performance_graph_util import *

if __name__ == '__main__':
    parent = '../rl2020_test_results/dqn-so/'
    parent_ppo = '../rl2020_test_results/ppo-so/'
    parent_mo_shared = '../rl2020_test_results/dqn-mo-shared/'
    parent_baseline = '../rl2020_test_results/baseline/'
    context['palette'] = 'PRGn' # 'cubehelix' #'husl', 'coolwarm', 'Blues', 'Reds', 'Greens' etc
    context['baseline_color'] = 'red'
    context['ylim'] = (0, .7)
    context['figsize'] = (15, 4)
    result_path = './dqn-performance/dqn-mo-performance-boxplot.pdf'
    data_sources = [
            BehaviourDataSource(label='dqn-mo-shared-random-20K', data_parent_path=parent_mo_shared + 
                                'dqn-mo-shared-random-20000-rb001-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw(data_sources, result_path)

    result_path = './dqn-performance/dqn-performance-boxplot.pdf'
    data_sources = [
            BehaviourDataSource(label='dqn-001', data_parent_path=parent + 'dqn-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-002', data_parent_path=parent + 'dqn-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-003', data_parent_path=parent + 'dqn-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-004', data_parent_path=parent + 'dqn-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-005', data_parent_path=parent + 'dqn-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-random', data_parent_path=parent + 'dqn-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw(data_sources, result_path)
        
    result_path = './dqn-performance/dqn-wtn-c700-performance-boxplot.pdf'
    data_sources = [
            BehaviourDataSource(label='dqn-wtn-c700-001', data_parent_path=parent + 'dqn-wtn-c700-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-002', data_parent_path=parent + 'dqn-wtn-c700-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-003', data_parent_path=parent + 'dqn-wtn-c700-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-004', data_parent_path=parent + 'dqn-wtn-c700-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-005', data_parent_path=parent + 'dqn-wtn-c700-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-random', data_parent_path=parent + 'dqn-wtn-c700-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw(data_sources, result_path)
    
    result_path = './dqn-performance/double-dqn-performance-boxplot.pdf'
    data_sources = [
            BehaviourDataSource(label='double-dqn-001', data_parent_path=parent + 'double-dqn-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-002', data_parent_path=parent + 'double-dqn-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-003', data_parent_path=parent + 'double-dqn-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-004', data_parent_path=parent + 'double-dqn-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-005', data_parent_path=parent + 'double-dqn-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-random', data_parent_path=parent + 'double-dqn-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]    
    draw(data_sources, result_path)
    
    result_path = './ppo-performance/ppo-performance-boxplot.pdf'
    context['ylim'] = (0, .035)
    data_sources = [
            BehaviourDataSource(label='ppo-001', data_parent_path=parent_ppo + 'ppo4K-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-002', data_parent_path=parent_ppo + 'ppo4K-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-003', data_parent_path=parent_ppo + 'ppo4K-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-004', data_parent_path=parent_ppo + 'ppo4K-004-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-005', data_parent_path=parent_ppo + 'ppo4K-005-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='ppo-random', data_parent_path=parent_ppo + 'ppo4K-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='baseline', data_parent_path=parent_baseline + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw(data_sources, result_path)
    