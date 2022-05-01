from rl2020_graph_generator.performance_graph_util import *

if __name__ == '__main__':
    parent = '../rl2020_test_results/'
    parent_q = '../rl2020_test_results/ql-so/'

    colors = ['#efffef', '#ccffe0', '#b2ffd0', '#99ffc1', '#00ff64', '#fff9b2', 'orange'] #https://www.w3schools.com/colors/colors_gradient.asp
    
    #colors = ['#e5ffef', '#ccffe0', '#b2ffd0', '#99ffc1', '#00ff64', '#e5feff', '#b2fcff', '#4cfaff', '#fff9b2', '#ffec00'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    result_path = './q-lambda-so/ql-performance.pdf'
    data_sources = [
            BehaviourDataSource(label='ql-001-200K', data_parent_path=parent_q + 'ql-001-200000-basic-a', num_trials=10),
            BehaviourDataSource(label='ql-002-200K', data_parent_path=parent_q + 'ql-002-200000-basic-a', num_trials=10),
            BehaviourDataSource(label='ql-003-200K', data_parent_path=parent_q + 'ql-003-200000-basic-a', num_trials=10),
            BehaviourDataSource(label='ql-004-200K', data_parent_path=parent_q + 'ql-004-200000-basic-a', num_trials=10),
            BehaviourDataSource(label='ql-005-200K', data_parent_path=parent_q + 'ql-005-200000-basic-a', num_trials=10),
            BehaviourDataSource(label='ql-random-200K', data_parent_path=parent_q + 'ql-random-200000-basic-a', num_trials=10),
            BehaviourDataSource(label='random-agent', data_parent_path=parent + 'random-agent-basic-a'),
            BehaviourDataSource(label='baseline', data_parent_path=parent + 'baseline/baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]    
    draw(data_sources, result_path)