from rl2020_graph_generator.performance_graph_util import *

if __name__ == '__main__':
    colors = ['lightgreen', 
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    #context['baseline_color'] = 'blue'
    parent1 = '../rl2020_test_results/'
    parent2 = '../rl2020_test_results/d2dspl/'
    result_path = './d2dspl-so/d2dspl-performance-boxplot.pdf'
    data_sources = [
#            BehaviourDataSource(label='ac-001-50K', data_parent_path=parent1 + 'ac-001-050000-basic-a'),
#            BehaviourDataSource(label='ac-002-50K', data_parent_path=parent1 + 'ac-002-050000-basic-a'),
#             BehaviourDataSource(label='ac-003-50K', data_parent_path=parent1 + 'ac-003-050000-basic-a'),
#             BehaviourDataSource(label='ac-004-50K', data_parent_path=parent1 + 'ac-004-050000-basic-a'),
#             BehaviourDataSource(label='ac-005-50K', data_parent_path=parent1 + 'ac-005-050000-basic-a'),
            BehaviourDataSource(label='ac-001-100K', data_parent_path=parent1 + 'ac-001-100000-basic-a'),
#            BehaviourDataSource(label='ac-002-100K', data_parent_path=parent1 + 'ac-002-100000-basic-a'),
#             BehaviourDataSource(label='ac-003-100K', data_parent_path=parent1 + 'ac-003-100000-basic-a'),
#             BehaviourDataSource(label='ac-004-100K', data_parent_path=parent1 + 'ac-004-100000-basic-a'),
#             BehaviourDataSource(label='ac-005-100K', data_parent_path=parent1 + 'ac-005-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-001-50K-5000', data_parent_path=parent2 + 'I/d2dspl-ac-001-050000-basic-a'),
#             BehaviourDataSource(label='d2dspl-001-50K-4000', data_parent_path=parent2 + 'H/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-50K-3000', data_parent_path=parent2 + 'G/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-50K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-100K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-001-100000-basic-a'),
            BehaviourDataSource(label='d2dspl-002-50K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-002-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-002-100K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-002-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-003-50K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-003-050000-basic-a'),
#             BehaviourDataSource(label='d2dspl-003-100K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-003-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-004-50K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-004-050000-basic-a'),
#             BehaviourDataSource(label='d2dspl-004-100K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-004-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-005-50K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-005-050000-basic-a'),
#             BehaviourDataSource(label='d2dspl-005-100K-2000', data_parent_path=parent2 + 'A/d2dspl-ac-005-100000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-1500', data_parent_path=parent2 + 'B/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-1000', data_parent_path=parent2 + 'C/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-500', data_parent_path=parent2 + 'D/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-300', data_parent_path=parent2 + 'E/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-200', data_parent_path=parent2 + 'F/d2dspl-ac-001-050000-basic-a'),

#            BehaviourDataSource(label='d2dspl-ac-002-50k-C', data_parent_path=parent2 + 'C/d2dspl-ac-002-050000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-001-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-001-020000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-002-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-002-020000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-001-100k', data_parent_path=parent + 'd2dspl-ac-001-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-002-100k', data_parent_path=parent + 'd2dspl-ac-002-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-003-100k', data_parent_path=parent + 'd2dspl-ac-003-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-004-100k', data_parent_path=parent + 'd2dspl-ac-004-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-005-100k', data_parent_path=parent + 'd2dspl-ac-005-100000-basic-a'),
            BehaviourDataSource(label='baseline', data_parent_path=parent1 + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw(data_sources, result_path)
    
    result_path = './d2dspl-so/original-d2dspl-performance-boxplot.pdf'
    data_sources = [
            BehaviourDataSource(label='ac-001-20K', data_parent_path=parent2 + 'ORG/ac-001-020000-basic-a'),
            BehaviourDataSource(label='ac-002-20K', data_parent_path=parent2 + 'ORG/ac-002-020000-basic-a'),
            BehaviourDataSource(label='ac-001-50K', data_parent_path=parent2 + 'ORG/ac-001-050000-basic-a'),
            #BehaviourDataSource(label='ac-002-50K', data_parent_path=parent2 + 'ORG/ac-002-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-ac-001-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-001-020000-basic-a'),
            BehaviourDataSource(label='d2dspl-ac-002-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-002-020000-basic-a'),
            BehaviourDataSource(label='baseline', data_parent_path=parent1 + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    #draw(data_sources, result_path)    