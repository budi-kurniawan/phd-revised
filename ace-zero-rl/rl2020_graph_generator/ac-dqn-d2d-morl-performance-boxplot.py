from rl2020_graph_generator.performance_graph_util import *

# gradient color codes: http://www.perbang.dk/rgb/00BABF/
if __name__ == '__main__':
    parent = '../rl2020_test_results/'
    parent_d2dsql = '../rl2020_test_results/d2dsql2/'
    parent_d2dspl = '../rl2020_test_results/d2dspl/'

    #https://www.w3schools.com/colors/colors_gradient.asp
    colors = ['LightCyan', 'LightSkyBlue', 'MediumBlue', #'Blue',
              '#f8f8f8', '#e8e8e8', '#d7d7d7', '#909090', '#808080', '#707070',
              'yellow', 'Turquoise', 'DarkTurquoise', 'LightSeaGreen',
              'LightGreen', 'MediumSpringGreen', 'GreenYellow', 'Green', 'LightGreen', 'MediumSpringGreen', 'GreenYellow', 'Green'] 
    context['palette'] = colors
    context['figsize'] = (15, 7.5)
#     context['figsize'] = (30, 19)    
    context['ylim'] = [0, 1.0]

    result_path = './ac-dqn-so/ac-dqn-d2d-morl-performance-boxplot-1.pdf'
    """ ac-004, ac-005, dqn-004 and dqn-005 are excluded because they are the worst among DQN agents """
    data_sources = [
            BehaviourDataSource(label='ac-001-200K', data_parent_path=parent + 'ac-so/ac-001-200000-basic-a'),
            BehaviourDataSource(label='ac-002-200K', data_parent_path=parent + 'ac-so/ac-002-200000-basic-a'),
#            BehaviourDataSource(label='ac-003-200K', data_parent_path=parent + 'ac-003-200000-basic-a'),
#             BehaviourDataSource(label='random-agent', data_parent_path=parent + 'random-agent-basic-a'),
            BehaviourDataSource(label='ac-random-200K', data_parent_path=parent + 'ac-so/ac-random-200000-basic-a'),
#             BehaviourDataSource(label='ac-random-500K', data_parent_path=parent + 'ac-random-500000-basic-a'),
#             BehaviourDataSource(label='ac-random-1M', data_parent_path=parent + 'ac-random-1000000-basic-a'),
            BehaviourDataSource(label='dqn-001-20K', data_parent_path=parent + 'dqn-so/dqn-001-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-002-20K', data_parent_path=parent + 'dqn-so/dqn-002-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-003-20K', data_parent_path=parent + 'dqn-so/dqn-003-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-random-20K', data_parent_path=parent + 'dqn-so/dqn-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='dqn-wtn-c700-random-20K', data_parent_path=parent + 'dqn-so/dqn-wtn-c700-random-20000-basic-a', num_trials=10),
            BehaviourDataSource(label='double-dqn-random-20K', data_parent_path=parent + 'dqn-so/double-dqn-random-20000-basic-a', num_trials=10),

            BehaviourDataSource(label='d2dspl', data_parent_path=parent_d2dspl + 'A/d2dspl-ac-001-050000-basic-a', num_trials=10),
            BehaviourDataSource(label='d2dsql-random-11K', data_parent_path=parent_d2dsql + 'A/d2dsql2-ac-random-011000-basic-a', num_trials=10),
            BehaviourDataSource(label='d2dsql-random-12K', data_parent_path=parent_d2dsql + 'A/d2dsql2-ac-random-012000-basic-a', num_trials=10),
            BehaviourDataSource(label='d2dsql-random-13K', data_parent_path=parent_d2dsql + 'A/d2dsql2-ac-random-013000-basic-a', num_trials=10),

            BehaviourDataSource(label='mo-ac-random-200K-rb004', data_parent_path=parent + 'ac-mo/ac-mo-random-001-200000-rb013-basic-a'),
            BehaviourDataSource(label='mo-ac-random-200K-rb005', data_parent_path=parent + 'ac-mo/ac-mo-random-001-200000-rb014-basic-a'),
            BehaviourDataSource(label='mo-ac-random-200K-rb006', data_parent_path=parent + 'ac-mo/ac-mo-random-001-200000-rb015-basic-a'),
            BehaviourDataSource(label='mo-ac-random-200K-rb007', data_parent_path=parent + 'ac-mo/ac-mo-random-001-500000-rb016-basic-a'),
            BehaviourDataSource(label='baseline', data_parent_path=parent + 'baseline/baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]    
    draw(data_sources, result_path)
    