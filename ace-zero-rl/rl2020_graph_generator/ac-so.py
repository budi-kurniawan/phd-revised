from rl2020_graph_generator.learning_graph_util import *

if __name__ == "__main__":
    #context['show_figures'] = True
    context['max_records'] = 200_000
    parent = '../rl2020_results/ac-so/'
    parent = '../rl2020_results/ac-so-500K/'
    image_paths = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (17000, 0.96)
    data_sources = [
            DataSource(name='ac-001', data_paths=[parent + 'ac-001'], labels=['ac-001'],
                       image_path=image_paths[0], image_xy=image_xy, result_path='./actor-critic-so/ac-001.png'),
            DataSource(name='ac-002', data_paths=[parent + 'ac-002'], labels=['ac-002'],
                       image_path=image_paths[1], image_xy=image_xy, result_path='./actor-critic-so/ac-002.png'),
#             DataSource(name='ac-003', data_paths=[parent + 'ac-003'], labels=['ac-003'],
#                        image_path=image_paths[2], image_xy=image_xy, result_path='./actor-critic-so/ac-003.png'),
#             DataSource(name='ac-004', data_paths=[parent + 'ac-004'], labels=['ac-004'],
#                        image_path=image_paths[3], image_xy=image_xy, result_path='./actor-critic-so/ac-004.png'),
#             DataSource(name='ac-005', data_paths=[parent + 'ac-005'], labels=['ac-005'],
#                        image_path=image_paths[4], image_xy=image_xy, result_path='./actor-critic-so/ac-005.png'),
            DataSource(name='ac-random-mistake', data_paths=[parent + 'ac-random-mistake002'], labels=['ac-random-mistake'],
                       result_path='./actor-critic-so/ac-random-mistake002.png'),

#             DataSource(name='ac-001bc', data_paths=[parent + 'ac-001', parent+'ac-001b', parent+'ac-001c'],
#                        labels=['ac-001 (Set 1)', 'ac-001 (Set 2)', 'ac-001 (Set 3)'],
#                        image_path=image_paths[0], image_xy=image_xy, result_path='./actor-critic-so/ac-001bc.pdf'),
#             DataSource(name='ac-002bc', data_paths=[parent + 'ac-002', parent+'ac-002b', parent+'ac-002c'],
#                        labels=['ac-002 (Set 1)', 'ac-002 (Set 2)', 'ac-002 (Set 3)'],
#                        image_path=image_paths[1], image_xy=image_xy, result_path='./actor-critic-so/ac-002bc.pdf'),
#             DataSource(name='ac-003bc', data_paths=[parent + 'ac-003', parent+'ac-003b', parent+'ac-003c'],
#                        labels=['ac-003 (Set 1)', 'ac-003 (Set 2)', 'ac-003 (Set 3)'],
#                        image_path=image_paths[2], image_xy=image_xy, result_path='./actor-critic-so/ac-003bc.pdf'),
#             DataSource(name='ac-004bc', data_paths=[parent + 'ac-004', parent+'ac-004b', parent+'ac-004c'],
#                        labels=['ac-004 (Set 1)', 'ac-004 (Set 2)', 'ac-004 (Set 3)'],
#                        image_path=image_paths[3], image_xy=image_xy, result_path='./actor-critic-so/ac-004bc.pdf'),
#             DataSource(name='ac-005bc', data_paths=[parent + 'ac-005', parent+'ac-005b', parent+'ac-005c'],
#                        labels=['ac-005 (Set 1)', 'ac-005 (Set 2)', 'ac-005 (Set 3)'],
#                        image_path=image_paths[4], image_xy=image_xy, result_path='./actor-critic-so/ac-005bc.pdf')
        ]
    #data_sources = data_sources[10:11]
    create_charts(data_sources)
    
    
    context['show_figures'] = True
    context['max_records'] = 1_000_000
    data_sources = [
    DataSource(name='ac-random-001', data_paths=[parent + 'ac-random-001'],
                       labels=['ac-random-001'], result_path='./actor-critic-so/ac-random-001.png')            
        ]
    #data_sources = data_sources[10:11]
    #create_charts(data_sources)