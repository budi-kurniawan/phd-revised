from rl2020_graph_generator.performance_graph_util import *

# gradient color codes: http://www.perbang.dk/rgb/00BABF/
if __name__ == '__main__':
    parent = '../rl2020_test_results/ac-so/'
    parent_b = '../rl2020_test_results/baseline/'
    parent_r = '../rl2020_test_results/'
    colors = ['#efffef', '#ccffe0', '#b2ffd0', '#99ffc1', '#00ff64', '#fff9b2', 'orange'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    result_path = './ac-so/ac-performance-boxplot-1.pdf'
    data_sources = [
        BehaviourDataSource(label='ac-001-200K', data_parent_path=parent + 'ac-001-200000-basic-a'),
        BehaviourDataSource(label='ac-002-200K', data_parent_path=parent + 'ac-002-200000-basic-a'),
        BehaviourDataSource(label='ac-003-200K', data_parent_path=parent + 'ac-003-200000-basic-a'),
        BehaviourDataSource(label='ac-004-200K', data_parent_path=parent + 'ac-004-200000-basic-a'),
        BehaviourDataSource(label='ac-005-200K', data_parent_path=parent + 'ac-005-200000-basic-a'),
        BehaviourDataSource(label='ac-random-200K', data_parent_path=parent + 'ac-random-200000-basic-a'),
        BehaviourDataSource(label='random-agent', data_parent_path=parent_r + 'random-agent-basic-a'),
        BehaviourDataSource(label='baseline', data_parent_path=parent_b + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
    ]    
    draw(data_sources, result_path)
#     data_sources = [
#             BehaviourDataSource(label='ac-001', data_parent_path=parent + 'ac-001-100000-basic-a'),
#             BehaviourDataSource(label='ac-002', data_parent_path=parent + 'ac-002-100000-basic-a'),
#             BehaviourDataSource(label='ac-003', data_parent_path=parent + 'ac-003-100000-basic-a'),
#             BehaviourDataSource(label='ac-004', data_parent_path=parent + 'ac-004-100000-basic-a'),
#             BehaviourDataSource(label='ac-005', data_parent_path=parent + 'ac-005-100000-basic-a'),
#             BehaviourDataSource(label='ac-random-100K', data_parent_path=parent + 'ac-random-100000-basic-a'),
#             BehaviourDataSource(label='ac-random-500K', data_parent_path=parent + 'ac-random-500000-basic-a'),
#             BehaviourDataSource(label='ac-random-1M', data_parent_path=parent + 'ac-random-1000000-basic-a'),
#             BehaviourDataSource(label='baseline', data_parent_path=parent + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
#         ]    
#    draw(data_sources, result_path)

#     result_path = './ac-so/ac-performance-boxplot-1b.pdf'
#     data_sources = [
#             BehaviourDataSource(label='ac-001-100K', data_parent_path=parent + 'ac-001-100000-basic-a'),
#             BehaviourDataSource(label='ac-001-200K', data_parent_path=parent + 'ac-001-200000-basic-a'),
#             BehaviourDataSource(label='ac-002-100K', data_parent_path=parent + 'ac-002-100000-basic-a'),
#             BehaviourDataSource(label='ac-002-200K', data_parent_path=parent + 'ac-002-200000-basic-a'),
#             BehaviourDataSource(label='ac-random-200K', data_parent_path=parent + 'ac-random-200000-basic-a'),
#             BehaviourDataSource(label='ac-random-500K', data_parent_path=parent + 'ac-random-500000-basic-a'),
#             BehaviourDataSource(label='ac-random-1M', data_parent_path=parent + 'ac-random-1000000-basic-a'),
#             BehaviourDataSource(label='baseline', data_parent_path=parent + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
#         ]    
#     draw(data_sources, result_path)

    
    result_path = './ac-so/ac-performance-boxplot-2.pdf'
    colors = ['#e5ffef', '#ccffe0', '#b2ffd0', '#99ffc1', '#00ff64', 'salmon', '#fff9b2', '#ffec00', '#ffbb00'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    context['figsize'] = (15, 10)
    data_sources = [
            BehaviourDataSource(label='ac-001-100K', data_parent_path=parent + 'ac-001-100000-basic-a'),
            BehaviourDataSource(label='ac-002-100K', data_parent_path=parent + 'ac-002-100000-basic-a'),
            BehaviourDataSource(label='ac-003-100K', data_parent_path=parent + 'ac-003-100000-basic-a'),
            BehaviourDataSource(label='ac-004-100K', data_parent_path=parent + 'ac-004-100000-basic-a'),
            BehaviourDataSource(label='ac-005-100K', data_parent_path=parent + 'ac-005-100000-basic-a'),
            BehaviourDataSource(label='ac-random-500K', data_parent_path=parent + 'ac-random-500000-basic-a'),
            BehaviourDataSource(label='ac-mp-001', data_parent_path=parent + 'ac-mp-001-100000-basic-a'),
            BehaviourDataSource(label='ac-mp-002', data_parent_path=parent + 'ac-mp-002-100000-basic-a'),
            BehaviourDataSource(label='ac-mp-003', data_parent_path=parent + 'ac-mp-003-100000-basic-a'),
            BehaviourDataSource(label='baseline', data_parent_path=parent + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]    
#     draw(data_sources, result_path)