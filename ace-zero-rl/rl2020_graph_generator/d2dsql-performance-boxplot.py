from rl2020_graph_generator.performance_graph_util import *

if __name__ == '__main__':
    colors = ['lightgreen', 'lightgreen', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'cyan', 'cyan', 'cyan', 'cyan', 'cyan', 
              'lightgreen', 'lightgreen', 'lightgreen','lightgreen', #'lightgreen','lightgreen', 'lightgreen',
              'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'white', 'white'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    #context['baseline_color'] = 'blue'
    parent1 = '../rl2020_test_results/'
    parent2 = '../rl2020_test_results/d2dspl/'
    parent3 = '../rl2020_test_results/d2dsql/'
    parent4 = '../rl2020_test_results/d2dsql2/'
    result_path = './d2dsql-so/d2dsql-performance-boxplot-landscape.pdf'
    data_sources = [
        BehaviourDataSource(label='ac-001-100K', data_parent_path=parent1 + 'ac-001-100000-basic-a'),
        BehaviourDataSource(label='ac-001-200K', data_parent_path=parent1 + 'ac-001-200000-basic-a'),
#         BehaviourDataSource(label='d2dspl-001-5000', data_parent_path=parent2 + 'I/d2dspl-ac-001-050000-basic-a'),
#         BehaviourDataSource(label='d2dspl-001-4000', data_parent_path=parent2 + 'H/d2dspl-ac-001-050000-basic-a'),
        BehaviourDataSource(label='d2dspl-001-3000', data_parent_path=parent2 + 'G/d2dspl-ac-001-050000-basic-a'),
        BehaviourDataSource(label='d2dspl-001-2000', data_parent_path=parent2 + 'A/d2dspl-ac-001-050000-basic-a'),
        BehaviourDataSource(label='ac-002-100K', data_parent_path=parent1 + 'ac-002-100000-basic-a'),
        BehaviourDataSource(label='ac-002-200K', data_parent_path=parent1 + 'ac-002-200000-basic-a'),

#         BehaviourDataSource(label='d2dspl-001-1500', data_parent_path=parent2 + 'B/d2dspl-ac-001-050000-basic-a'),
#         BehaviourDataSource(label='d2dspl-random-2000', data_parent_path=parent2 + 'A/d2dspl-ac-random-100000-basic-a'),
#         BehaviourDataSource(label='d2dspl-001-1000', data_parent_path=parent2 + 'C/d2dspl-ac-001-050000-basic-a'),
#         BehaviourDataSource(label='d2dspl-001-500', data_parent_path=parent2 + 'D/d2dspl-ac-001-050000-basic-a'),
#         BehaviourDataSource(label='d2dspl-001-300', data_parent_path=parent2 + 'E/d2dspl-ac-001-050000-basic-a'),
#         BehaviourDataSource(label='d2dspl-001-200', data_parent_path=parent2 + 'F/d2dspl-ac-001-050000-basic-a'),

        BehaviourDataSource(label='d2dspl-ac-002-50k-C', data_parent_path=parent2 + 'C/d2dspl-ac-002-050000-basic-a'),
#         BehaviourDataSource(label='d2dspl-ac-001-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-001-020000-basic-a'),
#         BehaviourDataSource(label='d2dspl-ac-002-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-002-020000-basic-a'),
        BehaviourDataSource(label='d2dspl-ac-001-100k', data_parent_path=parent2 + 'd2dspl-ac-001-100000-basic-a'),
        BehaviourDataSource(label='d2dspl-ac-002-100k', data_parent_path=parent2 + 'd2dspl-ac-002-100000-basic-a'),
        BehaviourDataSource(label='d2dspl-ac-003-100k', data_parent_path=parent2 + 'd2dspl-ac-003-100000-basic-a'),
        BehaviourDataSource(label='d2dspl-ac-004-100k', data_parent_path=parent2 + 'd2dspl-ac-004-100000-basic-a'),
        BehaviourDataSource(label='d2dspl-ac-005-100k', data_parent_path=parent2 + 'd2dspl-ac-005-100000-basic-a'),
        BehaviourDataSource(label='baseline', data_parent_path=parent1 + 'baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
    ]
#    draw(data_sources, result_path)

#    draw(data_sources, result_path)
    
    colors = ['lightgreen', 
              'yellow', 'yellow', 'cyan', 'cyan', 'cyan', 'cyan', 'cyan', 
              'lightgreen', 'lightgreen', 'lightgreen','lightgreen', #'lightgreen','lightgreen', 'lightgreen',
              'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'white', 'white'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    data_sources = [
#             BehaviourDataSource(label='ac-001-50K', data_parent_path=parent1 + 'ac-001-050000-basic-a'),
            BehaviourDataSource(label='ac-001-200K', data_parent_path=parent1 + 'ac-001-200000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-3000', data_parent_path=parent2 + 'G/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl-001-2000', data_parent_path=parent2 + 'A/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-10000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-001-010000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-11000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-001-011000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-12000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-001-012000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-13000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-001-013000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-14000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-001-014000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-100000-10000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-001-010000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-100000-11000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-001-011000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-100000-12000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-001-012000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-100000-13000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-001-013000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-100000-14000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-001-014000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-100000-15000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-001-015000-basic-a'),
            BehaviourDataSource(label='d2dsql-001-2000-100000-16000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-001-016000-basic-a'),
            BehaviourDataSource(label='d2dsql-002-2000-100000-10000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-002-010000-basic-a'),
            BehaviourDataSource(label='d2dsql-002-2000-100000-11000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-002-011000-basic-a'),
            BehaviourDataSource(label='d2dsql-002-2000-100000-12000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-002-012000-basic-a'),
            BehaviourDataSource(label='d2dsql-002-2000-100000-13000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-002-013000-basic-a'),
            BehaviourDataSource(label='d2dsql-002-2000-100000-14000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-002-014000-basic-a'),
            BehaviourDataSource(label='d2dsql-002-2000-100000-15000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-002-015000-basic-a'),
            BehaviourDataSource(label='d2dsql-002-2000-100000-16000 (fixed epsilon)', 
                                data_parent_path=parent4 + 'A/d2dsql2-ac-100000-002-016000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-10000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-010000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-11000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-011000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-12000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-012000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-13000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-013000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-14000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-014000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-15000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-015000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-16000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-016000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-17000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-017000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-18000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-018000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-19000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-019000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-20000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-020000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-10000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-010000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-11000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-011000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-12000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-012000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-13000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-013000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-14000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-014000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-15000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-015000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-16000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-016000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-10000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-010000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-11000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-011000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-12000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-012000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-13000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-013000-basic-a'),
            BehaviourDataSource(label='dqn-001-20000', data_parent_path=parent1 + '/dqn-001-20000-basic-a'),
            BehaviourDataSource(label='dqn-002-20000', data_parent_path=parent1 + '/dqn-002-20000-basic-a'),
            

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
    #draw(data_sources, result_path)    
    
    colors = ['#efffef', '#ddeedd',
              'yellow', 
              'PaleTurquoise', 'Turquoise', 'DarkTurquoise', 'LightSeaGreen',
              '#7b3294', '#c2a5cf', '#008837',
              'lightgreen', 'lightgreen', 'lightgreen','lightgreen', #'lightgreen','lightgreen', 'lightgreen',
              'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'white', 'white'] #https://www.w3schools.com/colors/colors_gradient.asp
    context['palette'] = colors
    context['figsize'] = (11, 12)
    context['figsize'] = (12, 7) # landscape
    data_sources = [
            BehaviourDataSource(label='ac-50K', data_parent_path=parent1 + 'ac-so/ac-random-100000-basic-a'),
            BehaviourDataSource(label='ac-001', data_parent_path=parent1 + 'ac-so/ac-001-200000-basic-a'),
            #BehaviourDataSource(label='d2dspl-001-3000', data_parent_path=parent2 + 'G/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dspl', data_parent_path=parent2 + 'A/d2dspl-ac-001-050000-basic-a'),
            BehaviourDataSource(label='d2dsql-random-10K', data_parent_path=parent4 + 'A/d2dsql2-ac-random-010000-basic-a'),
            BehaviourDataSource(label='d2dsql-random-11K', data_parent_path=parent4 + 'A/d2dsql2-ac-random-011000-basic-a'),
            BehaviourDataSource(label='d2dsql-random-12K', data_parent_path=parent4 + 'A/d2dsql2-ac-random-012000-basic-a'),
            BehaviourDataSource(label='d2dsql-random-13K', data_parent_path=parent4 + 'A/d2dsql2-ac-random-013000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-10K', data_parent_path=parent4 + 'A/d2dsql2-ac-001-010000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-11K', data_parent_path=parent4 + 'A/d2dsql2-ac-001-011000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-12K', data_parent_path=parent4 + 'A/d2dsql2-ac-001-012000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-13K', data_parent_path=parent4 + 'A/d2dsql2-ac-001-013000-basic-a'),
#             BehaviourDataSource(label='d2dsql-random-2000-14000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-random-014000-basic-a'),
#             BehaviourDataSource(label='d2dsql-random-2000-15000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-random-015000-basic-a'),
#             BehaviourDataSource(label='d2dsql-random-2000-16000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-random-016000-basic-a'),
#             BehaviourDataSource(label='d2dsql-random-2000-17000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-random-017000-basic-a'),
#             BehaviourDataSource(label='d2dsql-random-2000-18000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-random-018000-basic-a'),
#             BehaviourDataSource(label='d2dsql-random-2000-19000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-random-019000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-14000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-014000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-15000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-015000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-16000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-016000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-17000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-017000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-18000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-018000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-19000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-019000-basic-a'),
#             BehaviourDataSource(label='d2dsql-002-2000-20000 (fixed epsilon)', data_parent_path=parent4 + 'A/d2dsql2-ac-002-020000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-10000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-010000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-11000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-011000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-12000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-012000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-13000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-013000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-14000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-014000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-15000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-015000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1500-16000 (fixed epsilon)', data_parent_path=parent4 + 'B/d2dsql2-ac-001-016000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-10000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-010000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-11000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-011000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-12000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-012000-basic-a'),
#             BehaviourDataSource(label='d2dsql-001-1000-13000 (fixed epsilon)', data_parent_path=parent4 + 'C/d2dsql2-ac-001-013000-basic-a'),
            BehaviourDataSource(label='dqn-001', data_parent_path=parent1 + 'dqn-so/dqn-001-20000-basic-a'),
            BehaviourDataSource(label='dqn-002', data_parent_path=parent1 + 'dqn-so/dqn-002-20000-basic-a'),
            BehaviourDataSource(label='dqn-random', data_parent_path=parent1 + 'dqn-so/dqn-random-20000-basic-a'),
            

#            BehaviourDataSource(label='d2dspl-ac-002-50k-C', data_parent_path=parent2 + 'C/d2dspl-ac-002-050000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-001-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-001-020000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-002-20k-ORG', data_parent_path=parent2 + 'ORG/d2dspl-ac-002-020000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-001-100k', data_parent_path=parent + 'd2dspl-ac-001-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-002-100k', data_parent_path=parent + 'd2dspl-ac-002-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-003-100k', data_parent_path=parent + 'd2dspl-ac-003-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-004-100k', data_parent_path=parent + 'd2dspl-ac-004-100000-basic-a'),
#             BehaviourDataSource(label='d2dspl-ac-005-100k', data_parent_path=parent + 'd2dspl-ac-005-100000-basic-a'),
            BehaviourDataSource(label='baseline', data_parent_path=parent1 + 'baseline/baseline-blue-smart-pursuit-agent-basic-a', num_trials=1)
        ]
    draw(data_sources, result_path)