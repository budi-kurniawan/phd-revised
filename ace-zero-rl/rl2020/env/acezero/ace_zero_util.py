from ace_zero_core import utils
from ace_zero_core.utils import constrain_180, calc_ba_aa, get_aspect_angle, calc_los_angle, get_antenna_train_angle
import math

class Position(object):
    def __init__(self, x, y, psi, v=100):
        self.x = x
        self.y = y
        self.z = 0
        self.v = v
        self.theta = 0
        self.psi = psi


""" Returns h (head-on), n (neutral), d (defensive) or o (offensive). See Park's paper."""
def get_relative_position(blue, red):
    blue_pos = Position(blue[0], blue[1], blue[2])
    red_pos = Position(red[0], red[1], red[2])
    los1 = calc_los_angle(blue_pos.x, blue_pos.y, red_pos.x, red_pos.y)
    los2 = calc_los_angle(red_pos.x, red_pos.y, blue_pos.x, blue_pos.y)
    ba1, ba2, aa1, aa2 = calc_ba_aa(los1, los2, blue_pos.psi, red_pos.psi)
    #print(aa1, ba1)
    aa1 = math.fabs(aa1)
    ba1 = math.fabs(ba1)
    if aa1 >= 145 and ba1 <= 45:
        return 'h'
    elif ba1 >= 90:
        return 'n' if aa1 <= 90 else 'd'
    else:
        return 'o'


# def get_144_aa_ata_tuples(r=1500):
#     blue_x = 0 #r * math.cos(math.radians(blue_location_angle))
#     blue_y = 0 #r * math.sin(math.radians(blue_location_angle))
#     red_x = r
#     red_y= 0
#     angle_increase = 30
#     pairs = []
#     for blue_angle in range(0, 360, angle_increase):
#         blue_angle = constrain_180(blue_angle)
#         blue = (blue_x, blue_y, blue_angle)
#         for red_angle in range(0, 360, angle_increase):
#             red_angle = constrain_180(red_angle)
#             red = (red_x, red_y, red_angle)
# 
#             blue_pos = Position(blue[0], blue[1], blue[2])
#             red_pos = Position(red[0], red[1], red[2])
#             los1 = calc_los_angle(blue_pos.x, blue_pos.y, red_pos.x, red_pos.y)
#             los2 = calc_los_angle(red_pos.x, red_pos.y, blue_pos.x, blue_pos.y)
#             ba1, ba2, aa1, aa2 = calc_ba_aa(los1, los2, blue_pos.psi, red_pos.psi)
#             aa1 = math.fabs(aa1)
#             ba1 = math.fabs(ba1)
#             pairs.append((aa1, ba1))
#     return pairs


def get_144_initial_position_tuples(r=1500):
    blue_x = 0 #r * math.cos(math.radians(blue_location_angle))
    blue_y = 0 #r * math.sin(math.radians(blue_location_angle))
    red_x = r
    red_y= 0
    angle_increase = 30
    pairs = []
    for blue_angle in range(0, 360, angle_increase):
        blue_angle = constrain_180(blue_angle)
        blue = (blue_x, blue_y, blue_angle)
        for red_angle in range(0, 360, angle_increase):
            red_angle = constrain_180(red_angle)
            red = (red_x, red_y, red_angle)
            rel_pos = get_relative_position(blue, red)
            pairs.append((blue, red, rel_pos))
    return pairs

if __name__ == '__main__':
    pairs = get_144_initial_position_tuples()
    for pair in pairs:
        blue, red, rel_pos = pair
        print(blue, red, rel_pos)
        print('')
