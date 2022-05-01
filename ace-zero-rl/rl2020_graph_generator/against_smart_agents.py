import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import csv
import numpy as np
from collections import namedtuple
from matplotlib.ticker import FuncFormatter
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from rl2020.env.acezero.ace_zero_util import get_144_initial_position_tuples

""" Maybe improve to using 2D heatmap like this: https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib """

DataSource = namedtuple('DataSource', 'name data_paths result_path labels image_path image_xy', defaults=[None, None])
context = {'num_trials': 10, 'max_records': 100_000, 'num_avg_samples': 250, 'offset': 0.5, 'show_figures': False, 'ylim': (0, 1)}

def get_data(path):
    rounding_decimal = 6
    blue_scores = []
    red_scores = []
    with open(path,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            blue_scores.append(round(float(row[1]), rounding_decimal))
            red_scores.append(round(float(row[2]), rounding_decimal))
    return blue_scores, red_scores

def tick_label(x):
    if x % 45 == 0:
        return str(int(x)) + u'\N{DEGREE SIGN}'
    else:
        return ''
    
def create_charts(blue_scores, red_scores):
    plt.rcParams["figure.figsize"] = (7, 7)
    plt.rcParams["legend.loc"] = 'upper left'
    fig, ax = plt.subplots(1)
    ax.get_xaxis().set_major_formatter(FuncFormatter(lambda blue_x, p: tick_label(blue_x)))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda blue_x, p: tick_label(blue_x)))
    ax.set_xlim(context['xlim'])
    ax.set_ylim(context['ylim'])
    
    defensive_rects = []
    offensive_rects = []
    head_on_rect = []
    neutral_rects = []
    neutral_rects.append(Rectangle((-90, 90), 180, 90))
    neutral_rects.append(Rectangle((-90, -180), 180, 90))
    defensive_rects.append(Rectangle((-180, 90), 90, 90))
    defensive_rects.append(Rectangle((90, 90), 90, 90))
    defensive_rects.append(Rectangle((-180, -180), 90, 90))
    defensive_rects.append(Rectangle((90, -180), 90, 90))
    offensive_rects.append(Rectangle((-180, -90), 360, 180))
    head_on_rect.append(Rectangle((135, -45), 45, 90))
    head_on_rect.append(Rectangle((-180, -45), 45, 90))
    edgecolor='#000000'; alpha=0.6
    ax.add_collection(PatchCollection(offensive_rects, alpha=alpha, facecolor='#febebe', edgecolor=edgecolor, linewidth=(2,)))
    ax.add_collection(PatchCollection(head_on_rect, alpha=alpha, facecolor='#febebe', edgecolor=edgecolor, linewidth=(2,)))
    ax.add_collection(PatchCollection(defensive_rects, alpha=alpha, facecolor='#fafafa', edgecolor=edgecolor, linewidth=(2,)))
    ax.add_collection(PatchCollection(neutral_rects, alpha=alpha, facecolor='#dafeda', edgecolor=edgecolor, linewidth=(2,)))

    defensive_font = {'family': 'serif', 'color':  'blue', 'weight': 'bold', 'style': 'italic', 'size': 16,}
    offensive_font = {'family': 'serif', 'color':  'red', 'weight': 'bold', 'style': 'italic', 'size': 16,}
    head_on_font = {'family': 'serif', 'color':  'red', 'weight': 'bold', 'style': 'italic', 'size': 16,}
    neutral_font = {'family': 'serif', 'color':  'green', 'weight': 'bold', 'style': 'italic', 'size': 16,}
    plt.text(-33, 10, 'Offensive', fontdict=offensive_font)
    plt.text(160, 20, 'Head-on', fontdict=head_on_font, rotation='vertical')
    plt.text(-170, 20, 'Head-on', fontdict=head_on_font, rotation='vertical')
    plt.text(100, -139, 'Defensive', fontdict=defensive_font)    
    plt.text(100, 131, 'Defensive', fontdict=defensive_font)    
    plt.text(-170, -139, 'Defensive', fontdict=defensive_font)    
    plt.text(-170, 131, 'Defensive', fontdict=defensive_font)    
    plt.text(-28, 131, 'Neutral', fontdict=neutral_font)
    plt.text(-28, -139, 'Neutral', fontdict=neutral_font)    
    plt.margins(0, blue_x=None, blue_y=None, tight=True)
    plt.xlabel('AA')
    plt.ylabel('ATA')
    plt.xticks(np.arange(-180, 181, 15))
    plt.yticks(np.arange(-180, 181, 15))
    plt.grid(True)
    plt.tight_layout(pad=0.05) # will change ax dimension, make them bigger since margins are reduced        
    
    
    blue_x = []
    blue_y = []
    red_x = []
    red_y = []
    
    z1 = get_144_initial_position_tuples()
    #z2 = get_144_aa_ata_tuples()
    draws = 0
    for i in range(len(z1)): # [((0, 0, 0.0), (1500, 0, 0.0), 'o'), ((0, 0, 0.0), (1500, 0, 30.0), ...
        if z1[i][2] != 'ns':
            #s = (z1[i][1][2], z1[i][0][2])
            #print(i, z1[i], s)
            x = z1[i][1][2] # red's ATA = Blue's AA
            y = z1[i][0][2] # red's ATA = Blue's AA
            #x = x if x >= 0 else x + 360 # change -10 to 190 etc
            #y = y if y >= 0 else y + 360
            #print(x, y)
            if red_scores[i] < blue_scores[i]:
                blue_x.append(x) 
                blue_y.append(y)
            elif blue_scores[i] < red_scores[i]:
                red_x.append(x) 
                red_y.append(y)                
            else:
                draws += 1
    plt.scatter(blue_x, blue_y, marker='o', s=(100, ), facecolor='blue')
    plt.scatter(red_x, red_y, marker='o', s=(100, ), facecolor='red')
    
    print("Blue wins:", len(blue_x))
    print("Red wins:", len(red_x))
    print("Draws:", draws)
    plt.show()
            
if __name__ == '__main__':
    context['xlim'] = (-5, 190)
    context['ylim'] = (-5, 190)
    #path = '../rl2020_test_results/ac-random-1000000-red_pure_pursuit-basic-a/blue-red-scores-00.txt'
    #path = '../rl2020_test_results/ac-random-smart-pursuit-1000000-vs-red_smart_pursuit-basic-a/blue-red-scores-00.txt'
    #path = '../rl2020_test_results/ac-random-smart-pursuit-900000-vs-red_smart_pursuit-basic-a/blue-red-scores-00.txt'
    #path = '../rl2020_test_results/ac-random-smart-pursuit-1000000-vs-red_pure_pursuit-basic-a/blue-red-scores-00.txt'
    #path = '../rl2020_test_results/ac-random-1000000-red_restricted_pure_pursuit-basic-a/blue-red-scores-00.txt'
    #path = '../rl2020_test_results/ac-mo-random-500000-rb013-red_restricted_pure_pursuit-basic-a/blue-red-scores-02.txt'
    #path = '../rl2020_test_results/ac-mo-random-500000-rb013-red_restricted_smart_pursuit-basic-a/blue-red-scores-02.txt'
    #path = '../rl2020_test_results/ac-mo-random-500000-rb013-red_restricted_stern_conversion-basic-a/blue-red-scores-02.txt'
    path = '../rl2020_test_results/ac-random-1000000-vs-ac-random-1000000-basic-a/blue-red-scores-09.txt'
    #path = '../rl2020_test_results/ac-random-500000-vs-ac-mo-random-500000-rb013-basic-a/blue-red-scores-02.txt'
    #path = '../rl2020_test_results/ac-mo-random-500000-rb013-vs-ac-random-1000000-basic-a/blue-red-scores-03.txt'
    #path = '../rl2020_test_results/ac-mo-random-500000-rb013-vs-ac-mo-random-500000-rb013-basic-a/blue-red-scores-00.txt'
    
    data = get_data(path)
    blue_scores = data[0]
    red_scores = data[1]
    create_charts(blue_scores, red_scores)