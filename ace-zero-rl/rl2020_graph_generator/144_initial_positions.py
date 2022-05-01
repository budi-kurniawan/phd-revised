import math
import matplotlib.pyplot as plt
from rl2020.env.acezero.ace_zero_util import get_144_initial_position_tuples

def adjust_arrow_size(arrow_length, arrow_width, head_length, head_width, angle):
    abs_angle = math.fabs(angle)
    if abs_angle == 0 or abs_angle == 180:
        return arrow_length, arrow_width, head_length, head_width
    if abs_angle == 30 or abs_angle==150:
        return 1.1 * arrow_length, 0.8 * arrow_width, 1.1 * head_length, 0.8 * head_width
    if abs_angle == 60 or abs_angle ==120:
        return 1.5 * arrow_length, 0.6 * arrow_width, 1.5 * head_length, 0.6 * head_width
    return 2.2 * arrow_length, 0.3 * arrow_width, 2 * head_length, 0.4 * head_width

def get_x_offset(arrow_length, angle):
    return arrow_length * (1 - math.cos(angle)) / 2

if __name__ == '__main__':
    label_colors = {'o':'blue', 'd':'gray', 'n':'black', 'h':'red'}
    label_bg_colors = {'o':'yellow', 'd':'white', 'n':'#dedede', 'h':'#66ff22'}
    arrow_length = 6
    arrow_width = 1.5
    head_width = 4.90
    head_length = 2
    max_y = 350
    alpha = 0.5
    label_text_size = 9
    label_y_offset = 18
    plot_size = 160
    plt.xlim(-5, 250)
    plt.ylim(-5, max_y + 30)
    plt.gcf().set_size_inches(plot_size, plot_size)
#     plt.xticks([])
#     plt.yticks([])
    shape='right'
    arrow_params = {'length_includes_head': True, 'shape': shape, 'head_starts_at_zero': False}

    positions = get_144_initial_position_tuples(1500)
    distance_btw_arrows = 8
    count = 0 # 0, 48 or 96
    for row in range(0, 8):
        for column in range(0, 6):
            pos = positions[count]
            blue_pos, red_pos, behavior = pos[0], pos[1], pos[2]
            blue_angle, red_angle = blue_pos[2], red_pos[2]
            y = row * 44
            x = column * 20
            
            blue_arrow_length, blue_arrow_width, blue_head_length, blue_head_width = \
                    adjust_arrow_size(arrow_length, arrow_width, head_length, head_width, blue_angle)
            red_arrow_length, red_arrow_width, red_head_length, red_head_width = \
                    adjust_arrow_size(arrow_length, arrow_width, head_length, head_width, red_angle)
            blue_angle = math.radians(blue_angle)
            red_angle = math.radians(red_angle)
            blue_x_offset = get_x_offset(arrow_length, blue_angle)
            red_x_offset = get_x_offset(arrow_length, red_angle)
            
            plt.arrow(x + blue_x_offset, max_y - y, blue_arrow_length * math.cos(blue_angle), blue_arrow_length * math.sin(blue_angle), 
                      fc='b', ec='b', width=blue_arrow_width, head_length=blue_head_length, head_width=blue_head_width, **arrow_params)
            plt.arrow(x + red_x_offset + distance_btw_arrows, max_y - y, red_arrow_length * math.cos(red_angle), red_arrow_length * math.sin(red_angle), 
                      fc='r', ec='r', width=red_arrow_width, head_length=red_head_length, head_width=red_head_width, **arrow_params)
            
            count+=1
            label = str(count) + ' - ' + behavior
            plt.text(x + 7, max_y - y + label_y_offset, label, size=label_text_size, ha='center', va='center',
                 color=label_colors[behavior], weight='bold', 
                 bbox=dict(facecolor=label_bg_colors[behavior], alpha=1, boxstyle="square,pad=0.15"))
    #plt.margins(100, x=None, y=None, tight=True)
    plt.tight_layout(pad=5) # will change ax dimension, make them bigger since margins are reduced        
    plt.show()