from rl2020_graph_generator.learning_graph_util import *

if __name__ == "__main__":
#     num_trials = 10
#     num_avg_samples = 250  # how many samples to average for each data point in the x axis. If the value is 1, no averaging is done
#     offset = 0.5
    context['show_figures'] = True
    context['max_records'] = 200_000
    parent_ql = '../rl2020_results/ql-so-200K/'
    parent_ac = '../rl2020_results/ac-so-500K/'
    images = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (27500, 0.755)
    data_sources = [
        DataSource(name='ac-001', data_paths=[parent_ql + 'ql-001', parent_ac + 'ac-001'], labels=['ql-001', 'ac-001'],
            image_path='../data/img/init-pos-1.png', image_xy=image_xy, result_path='./ql-vs-ac-so/ql-ac-001.pdf', title='Initial Position: 001'),
        DataSource(name='ac-002', data_paths=[parent_ql + 'ql-002', parent_ac + 'ac-002'], labels=['ql-002', 'ac-002'],
            image_path='../data/img/init-pos-2.png', image_xy=image_xy, result_path='./ql-vs-ac-so/ql-ac-002.pdf', title='Initial Position: 002'),
        DataSource(name='ac-003', data_paths=[parent_ql + 'ql-003', parent_ac + 'ac-003'], labels=['ql-003', 'ac-003'],
            image_path='../data/img/init-pos-3.png', image_xy=image_xy, result_path='./ql-vs-ac-so/ql-ac-003.pdf', title='Initial Position: 003'),
        DataSource(name='ac-004', data_paths=[parent_ql + 'ql-004', parent_ac + 'ac-004'], labels=['ql-004', 'ac-004'],
            image_path='../data/img/init-pos-4.png', image_xy=image_xy, result_path='./ql-vs-ac-so/ql-ac-004.pdf', title='Initial Position: 004'),
        DataSource(name='ac-005', data_paths=[parent_ql + 'ql-005', parent_ac + 'ac-005'], labels=['ql-005', 'ac-005'],
            image_path='../data/img/init-pos-5.png', image_xy=image_xy, result_path='./ql-vs-ac-so/ql-ac-005.pdf', title='Initial Position: 005'),            
        DataSource(name='ac-random', data_paths=[parent_ql + 'ql-random', parent_ac + 'ac-random'], labels=['ql-random', 'ac-random'], 
                   result_path='./ql-vs-ac-so/ql-ac-random.pdf', title='Initial Position: Random')
    ]
    #data_sources = data_sources[10:11]
    create_charts(data_sources)
    
#     image_xy = (26000, 0.96)
#     data_sources = [
#             DataSource(name='ql-random-1M', data_paths=[parent_ql + 'ql-random-001'], labels=['ql-random'], 
#                        result_path='./ql-vs-ac-so/ql-random.pdf')
#         ]
#     create_charts(data_sources)    