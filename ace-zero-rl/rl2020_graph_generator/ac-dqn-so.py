from rl2020_graph_generator.learning_graph_util import *

if __name__ == "__main__":
    context['show_figures'] = True
    context['max_records'] = 200_000
    context['legend.loc'] = 'upper center'
    #parent_ac = '../rl2020_results/ac-so/'
    parent_ac = '../rl2020_results/ac-so-500K/'
    parent_dqn = '../rl2020_results/dqn-so/'

    image_paths = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (13800, 0.97)
        
    data_sources = [
            DataSource(name='ac-dqn-001', data_paths=[parent_ac + 'ac-001', parent_dqn + 'dqn-001'], labels=['ac-001', 'dqn-001'],
                       image_path=image_paths[0], image_xy=image_xy, result_path='./ac-dqn-so/ac-dqn-001.pdf'),
            DataSource(name='ac-dqn-002', data_paths=[parent_ac + 'ac-002', parent_dqn + 'dqn-002'], labels=['ac-002', 'dqn-002'],
                       image_path=image_paths[1], image_xy=image_xy, result_path='./ac-dqn-so/ac-dqn-002.pdf'),
            DataSource(name='ac-dqn-003', data_paths=[parent_ac + 'ac-003', parent_dqn + 'dqn-003'], labels=['ac-003', 'dqn-003'],
                       image_path=image_paths[2], image_xy=image_xy, result_path='./ac-dqn-so/ac-dqn-003.pdf'),
            DataSource(name='ac-dqn-004', data_paths=[parent_ac + 'ac-004', parent_dqn + 'dqn-004'], labels=['ac-004', 'dqn-004'],
                       image_path=image_paths[3], image_xy=image_xy, result_path='./ac-dqn-so/ac-dqn-004.pdf'),
            DataSource(name='ac-dqn-005', data_paths=[parent_ac + 'ac-005', parent_dqn + 'dqn-005'], labels=['ac-005', 'dqn-005'],
                       image_path=image_paths[4], image_xy=image_xy, result_path='./ac-dqn-so/ac-dqn-005.pdf'),
            DataSource(name='ac-dqn-random', data_paths=[parent_ac + 'ac-random', parent_dqn + 'dqn-random'], labels=['ac-random', 'dqn-random'],
                       result_path='./ac-dqn-so/ac-dqn-random.pdf'),
        ]
    data_sources = data_sources[5:6]
    create_charts(data_sources)