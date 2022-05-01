from rl2020_graph_generator.learning_graph_util import *

if __name__ == "__main__":
    context['show_figures'] = True
    context['num_avg_samples'] = 50
    #context['ylim'] = (0, 0.2)
    parent = '../rl2020_results/'

    images = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (3830, 0.96)
    data_sources = [
        DataSource(name='dqn-wtn-c700-001', data_paths=[parent + 'dqn-wtn-c700-001'], labels=['dqn-wtn-c700-001'],
                   image_path=images[0], image_xy=image_xy, result_path='./dqn-so/dqn-wtn-c700-001.png'),
        DataSource(name='dqn-wtn-c700-002', data_paths=[parent + 'dqn-wtn-c700-002'], labels=['dqn-wtn-c700-002'],
                   image_path=images[1], image_xy=image_xy, result_path='./dqn-so/dqn-wtn-c700-002.png'),
        DataSource(name='dqn-wtn-c700-003', data_paths=[parent + 'dqn-wtn-c700-003'], labels=['dqn-wtn-c700-003'],
                   image_path=images[2], image_xy=image_xy, result_path='./dqn-so/dqn-wtn-c700-003.png'),
        DataSource(name='dqn-wtn-c700-004', data_paths=[parent + 'dqn-wtn-c700-004'], labels=['dqn-wtn-c700-004'],
                   image_path=images[3], image_xy=image_xy, result_path='./dqn-so/dqn-wtn-c700-004.png'),
        DataSource(name='dqn-wtn-c700-005', data_paths=[parent + 'dqn-wtn-c700-005'], labels=['dqn-wtn-c700-005'],
                   image_path=images[4], image_xy=image_xy, result_path='./dqn-so/dqn-wtn-c700-005.png'),
        DataSource(name='dqn-wtn-c700-random', data_paths=[parent + 'dqn-wtn-c700-random'], labels=['dqn-wtn-c700-random'],
                   result_path='./dqn-so/dqn-wtn-c700-random.png')
    ]
    #data_sources = data_sources[10:11]
    #create_charts(data_sources)
    
    
    image_xy = (3530, 0.96)
    data_sources = [
        DataSource(name='double-dqn-001', data_paths=[parent + 'double-dqn-001'], labels=['double-dqn-001'],
                   image_path=images[0], image_xy=image_xy, result_path='./dqn-so/double-dqn-001.png'),
        DataSource(name='double-dqn-002', data_paths=[parent + 'double-dqn-002'], labels=['double-dqn-002'],
                   image_path=images[1], image_xy=image_xy, result_path='./dqn-so/double-dqn-002.png'),
        DataSource(name='double-dqn-003', data_paths=[parent + 'double-dqn-003'], labels=['double-dqn-003'],
                   image_path=images[2], image_xy=image_xy, result_path='./dqn-so/double-dqn-003.png'),
        DataSource(name='double-dqn-004', data_paths=[parent + 'double-dqn-004'], labels=['double-dqn-004'],
                   image_path=images[3], image_xy=image_xy, result_path='./dqn-so/double-dqn-004.png'),
        DataSource(name='double-dqn-005', data_paths=[parent + 'double-dqn-005'], labels=['double-dqn-005'],
                   image_path=images[4], image_xy=image_xy, result_path='./dqn-so/double-dqn-005.png'),
        DataSource(name='double-dqn-random', data_paths=[parent + 'double-dqn-random'], labels=['double-dqn-random'],
                   result_path='./dqn-so/double-dqn-random.png')
    ]
    #data_sources = data_sources[10:11]
    create_charts(data_sources)    