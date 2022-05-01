from rl2020_graph_generator.learning_graph_util import *

if __name__ == "__main__":
    context['show_figures'] = True
    context['num_avg_samples'] = 50
    context['max_records'] = 20000
    #context['ylim'] = (0, 0.2)
    parent = '../rl2020_results/'
    parent = '../rl_results/'

    images = ['../data/img/init-pos-1.png', '../data/img/init-pos-2.png', '../data/img/init-pos-3.png', 
              '../data/img/init-pos-4.png', '../data/img/init-pos-5.png']

    image_xy = (3000, 0.96)
    """ charts for 2020 paper """
    data_sources = [
            DataSource(name='d2dsql-002', data_paths=[parent + 'd2dsql-002.json', parent+'double-dqn-001.json'],
                       labels=['d2dsql-af', 'ddqn'], result_path='./d2dsql-so/2020paper-d2dsql-af.pdf'),
            DataSource(name='d2dsql-002f', data_paths=[parent + 'd2dsql-002f.json', parent+'double-dqn-001.json'],
                       labels=['d2dsql-fe', 'ddqn'], result_path='./d2dsql-so/2020paper-d2dsql-fe.pdf')
        ]
    #data_sources = data_sources[10:11]
    #create_charts(data_sources)
    
    
    image_xy = (3900, 0.97)
    parent = '../rl2020_results/dqn-so/'
    parent1 = '../rl2020_results/d2dsql/'
    parent2 = '../rl2020_results/d2dsql2/'
    data_sources = [
            DataSource(name='d2dsql-001-2000', data_paths=[parent1 + 'A/d2dsql-001', parent2 + 'A/d2dsql2-001', parent+'dqn-001'],
                       labels=['d2dsql-001-2000-af', 'd2dsql-001-2000-fe', 'DQN 001'], 
                       image_path=images[0], image_xy=image_xy, result_path='./d2dsql-so/d2dsql-001-2000-af-fe.pdf'),
            DataSource(name='d2dsql-001-1500', data_paths=[parent1 + 'B/d2dsql-001', parent2 + 'B/d2dsql2-001', parent+'dqn-001'],
                       labels=['d2dsql-001-1500-af', 'd2dsql-001-1500-fe', 'DQN 001'],
                       image_path=images[0], image_xy=image_xy, result_path='./d2dsql-so/d2dsql-001-1500-af-fe.pdf')
        ]
    #data_sources = data_sources[10:11]
    create_charts(data_sources)    