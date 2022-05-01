from rl2020.discretizer.discretizer import Discretizer

from rl2020.util.util import override

class AceZeroDiscretizer14000(Discretizer):
    @override(Discretizer)
    def get_num_discrete_states(self):
        return 14_000

    @override(Discretizer)
    def get_num_state_variables(self):
        return 4 # distance, contact_aa, contact_ata, delta_v
    
    @override(Discretizer)
    def discretize(self, state):
        distance_btw_arrows, contact_aa, contact_ata, delta_v = state
        R = distance_btw_arrows // 200
        if R > 13:
            R = 13
        aa = self.discretize_degrees(contact_aa)   # 0..9
        ata = self.discretize_degrees(contact_ata) # 0..9
        dv = self.discretize_delta_v(delta_v)      # 0..9
        return int(R * 1000 + dv * 100 + aa * 10 + ata) # 14,000 combinations
    
    def discretize_degrees(self, degrees):
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
    
    def discretize_delta_v(self, delta_v):
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