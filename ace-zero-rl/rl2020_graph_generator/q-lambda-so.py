from rl2020_graph_generator.learning_graph_util import *

if __name__ == "__main__":
    #context['show_figures'] = True
    #context['ylim'] = (0, 0.2)
    parent = '../rl2020_results/'

    image_paths = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (14000, 0.96)
    data_sources = [
            DataSource(name='ql-001', data_paths=[parent + 'ql-001'], labels=['ql-001'],
                       image_path=image_paths[0], image_xy=image_xy, result_path='./q-lambda-so/ql-001.png'),
            DataSource(name='ql-002', data_paths=[parent + 'ql-002'], labels=['ql-002'],
                       image_path=image_paths[1], image_xy=image_xy, result_path='./q-lambda-so/ql-002.png'),
            DataSource(name='ql-003', data_paths=[parent + 'ql-003'], labels=['ql-003'],
                       image_path=image_paths[2], image_xy=image_xy, result_path='./q-lambda-so/ql-003.png'),
            DataSource(name='ql-004', data_paths=[parent + 'ql-004'], labels=['ql-004'],
                       image_path=image_paths[3], image_xy=image_xy, result_path='./q-lambda-so/ql-004.png'),
            DataSource(name='ql-005', data_paths=[parent + 'ql-005'], labels=['ql-005'],
                       image_path=image_paths[4], image_xy=image_xy, result_path='./q-lambda-so/ql-005.png')
        ]
    #data_sources = data_sources[10:11]
    create_charts(data_sources)
    
    
    
    context['max_records'] = 1_000_000
    data_sources = [
    DataSource(name='ql-random-001', data_paths=[parent + 'ql-random-001'],
                       labels=['ql-random-001'], result_path='./q-lambda-so/ql-random-001.png')            
        ]
    create_charts(data_sources)