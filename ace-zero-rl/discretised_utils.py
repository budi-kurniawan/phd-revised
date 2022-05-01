#import numpy as np
# def softmax(x):
#     e_x = np.exp(x - np.max(x))
#     return e_x / e_x.sum(axis=0) 
# 
# def select_action(theta, state, actions):
#     discrete_state = discretise_state(state);
#     prob = softmax(theta[discrete_state])
#     return np.random.choice(actions, p=prob)

def discretise_degrees(degrees):
    if degrees <= 10 and degrees >= -10:
        return 0
    if degrees > 10 and degrees <= 30:
        return 1
    if degrees < -10 and degrees >= -30:
        return 2
    if degrees > 30 and degrees <= 50:
        return 3
    if degrees < -30 and degrees >= -50:
        return 4
    if degrees > 50 and degrees <= 70:
        return 5
    if degrees < -50 and degrees >= -70:
        return 6
    if degrees > 70 and degrees <= 90:
        return 7
    if degrees < -70 and degrees >= -90:
        return 8;
    return 9;

def discretise_delta_v(delta_v):
    if delta_v > 20:
        return 0
    if delta_v > 15:
        return 1
    if delta_v > 10:
        return 2
    if delta_v > 5:
        return 3
    if delta_v > 0:
        return 4
    if delta_v > -5:
        return 5
    if delta_v > -10:
        return 6
    if delta_v > -15:
        return 7
    if delta_v > -20:
        return 8
    return 9
    
def discretise_state(state):
    distance_btw_arrows, contact_aa, contact_ata, delta_v = state
    R = distance_btw_arrows // 200
    if R > 13:
        R = 13
    aa = discretise_degrees(contact_aa)   # 0..9
    ata = discretise_degrees(contact_ata) # 0..9
    dv = discretise_delta_v(delta_v)      # 0..9
    return int(R * 1000 + dv * 100 + aa * 10 + ata) # 14,000 combinations
