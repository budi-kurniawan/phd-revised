from rl2020.discretizer.discretizer import Discretizer

FOURTHIRDS = 1.3333333333333
ONE_DEGREE = 0.0174532 # 2pi/360
SIX_DEGREES = 0.1047192
TWELVE_DEGREES = 0.2094384
FIFTY_DEGREES = 0.87266

class CartpoleDiscretizer(Discretizer):
    def discretize(self, state):
        x, x_dot, theta, theta_dot = state
        discrete_x = 0 if x < -0.8 else (1 if x < 0.8 else 2)
        discrete_x_dot = 0 if x_dot < -0.5 else (1 if x_dot < 0.5 else 2)
        discrete_theta_dot = 0 if theta_dot < -FIFTY_DEGREES else (1 if theta_dot < FIFTY_DEGREES else 2)
        
        discrete_theta = None
        if theta < -SIX_DEGREES:
            discrete_theta = 0
        elif theta < -ONE_DEGREE:
            discrete_theta = 1
        elif theta < 0:
            discrete_theta = 2
        elif theta < ONE_DEGREE:
            discrete_theta = 3
        elif theta < SIX_DEGREES:
            discrete_theta = 4
        else:
            discrete_theta = 5;
        return (discrete_theta * 3 * 3 * 3 + discrete_theta_dot * 3 * 3 + discrete_x_dot * 3 + discrete_x)
    
    def get_num_discrete_states(self):
        return 162