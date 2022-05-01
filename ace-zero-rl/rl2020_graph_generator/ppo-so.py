from rl2020_graph_generator.learning_graph_util import *

if __name__ == "__main__":
    context['show_figures'] = True
    context['num_avg_samples'] = 50
    #context['ylim'] = (0, 0.2)
    parent_ppo = '../rl2020_results/ppo-so/'
    parent_dqn = '../rl2020_results/dqn-so/'

    images = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (3000, 0.755)
    context['colors'] = ['blue', 'brown']
    context['edgecolors'] = ['lightblue', 'brown']
    context['facecolors'] = ['lightblue', 'brown']

    data_sources = [
            DataSource(name='001', data_paths=[parent_dqn + 'dqn-001', parent_ppo + 'ppo4K-001'], 
                       labels=['dqn-001', 'ppo-001'],
                       image_path=images[0], image_xy=image_xy, result_path='./ppo-so/dqn-ppo4K-001.pdf'),
            DataSource(name='002', data_paths=[parent_dqn + 'dqn-002', parent_ppo + 'ppo4K-002'],
                       labels=['dqn-002', 'ppo-002'],
                       image_path=images[1], image_xy=image_xy, result_path='./ppo-so/dqn-ppo4K-002.pdf'),
            DataSource(name='003', data_paths=[parent_dqn + 'dqn-003', parent_ppo + 'ppo4K-003'],
                       labels=['dqn-003', 'ppo-003'],
                       image_path=images[2], image_xy=image_xy, result_path='./ppo-so/dqn-ppo4K-003.pdf'),
            DataSource(name='004', data_paths=[parent_dqn + 'dqn-004', parent_ppo + 'ppo4K-004'],
                       labels=['dqn-004', 'ppo-004'],
                       image_path=images[3], image_xy=image_xy, result_path='./ppo-so/dqn-ppo4K-004.pdf'),
            DataSource(name='005', data_paths=[parent_dqn + 'dqn-005', parent_ppo + 'ppo4K-005'],
                       labels=['dqn-005', 'ppo-005'],
                       image_path=images[0], image_xy=image_xy, result_path='./ppo-so/dqn-ppo4K-005.pdf'),
            DataSource(name='random', data_paths=[parent_dqn + 'dqn-random', parent_ppo + 'ppo4K-random'],
                       labels=['dqn-random', 'ppo-random'],
                       result_path='./ppo-so/dqn-ppo4K-random.pdf')
        ]
    create_charts(data_sources)

    image_xy = (3950, 0.755)
#     data_sources = [
#         DataSource(name='dqn-001', data_paths=[parent_dqn + 'dqn-001', parent_dqnwtn + 'dqn-wtn-c700-001', parent_ddqn +'double-dqn-001'],
#             labels=['dqn-001', 'dqn-wtn-c700-001', 'double-dqn-001'], image_path=images[0], image_xy=image_xy, 
#             result_path='./dqn-so/dqn-dqnwtn-double-dqn-001.pdf', title='Initial Position: 001'),
#         DataSource(name='dqn-002', data_paths=[parent_dqn + 'dqn-002', parent_dqnwtn + 'dqn-wtn-c700-002', parent_ddqn + 'double-dqn-002'],
#             labels=['dqn-002', 'dqn-wtn-c700-002', 'double-dqn-002'], image_path=images[1], image_xy=image_xy, 
#             result_path='./dqn-so/dqn-dqnwtn-double-dqn-002.pdf', title='Initial Position: 002'),
#         DataSource(name='dqn-003', data_paths=[parent_dqn + 'dqn-003', parent_dqnwtn + 'dqn-wtn-c700-003', parent_ddqn + 'double-dqn-003'],
#             labels=['dqn-003', 'dqn-wtn-c700-003', 'double-dqn-003'], image_path=images[2], image_xy=image_xy, 
#             result_path='./dqn-so/dqn-dqnwtn-double-dqn-003.pdf', title='Initial Position: 003'),
#         DataSource(name='dqn-004', data_paths=[parent_dqn + 'dqn-004', parent_dqnwtn + 'dqn-wtn-c700-004', parent_ddqn + 'double-dqn-004'],
#             labels=['dqn-004', 'dqn-wtn-c700-004', 'double-dqn-004'], image_path=images[3], image_xy=image_xy, 
#             result_path='./dqn-so/dqn-dqnwtn-double-dqn-004.pdf', title='Initial Position: 004'),
#         DataSource(name='dqn-005', data_paths=[parent_dqn + 'dqn-005', parent_dqnwtn + 'dqn-wtn-c700-005', parent_ddqn + 'double-dqn-005'],
#             labels=['dqn-005', 'dqn-wtn-c700-005', 'double-dqn-005'], image_path=images[4], image_xy=image_xy, 
#             result_path='./dqn-so/dqn-dqnwtn-double-dqn-005.pdf', title='Initial Position: 005'),
#     ]
#     #data_sources = data_sources[10:11]
#     #create_charts(data_sources)
#     
#     
#     data_sources = [
#             DataSource(name='dqn-random', data_paths=[parent_dqn + 'dqn-random', parent_dqnwtn + 'dqn-wtn-c700-random', parent_ddqn + 'double-dqn-random'],
#                        labels=['dqn-random', 'dqn-wtn-c700-random', 'double-dqn-random'],
#                        result_path='./dqn-so/dqn-dqnwtn-double-dqn-random.pdf', title='Initial Position: Random'),
#     ]
#     create_charts(data_sources)

    ''' ppo instability --> ppo4K-001 start_trial 6, ppo4K-002, 3, ppo4K-004, 1, ppo4K-004, 4'''
    context['num_trials'] = 1
    context['start_trial'] = 3
    context['ylim'] = (0, 1)
    context['figsize'] = (14, 3.6)
    context['colors'] = ['brown']
    data_sources = [
            DataSource(name='ppo', data_paths=[parent_ppo + 'ppo4K-random'],
                       labels=['ppo-random (trial 3)'],
                       result_path='./ppo-so/ppo-instability.pdf', title=''),
    ]
    create_charts(data_sources)
