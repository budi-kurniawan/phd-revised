from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

""" must be used in conjunction with AceZeroEnvironmentRewardBuilder101"""
class AceZeroMORLRewardBuilder101(RewardBuilder):
    @override(RewardBuilder)
    def get_rewards(self, data):
        viper = data.get('viper', None)
        current_time = data.get('current_time', None)
        #dt = data.get('dt', None)
        r = viper.contact_range
        aa = viper.contact_aa
        ata = viper.contact_ata        
        desired_position = r > 152 and r < 914 and abs(aa) < 30 and abs(ata) < 30        
        self.t = self.t + 1 if desired_position else 0
        r1 = viper.mcgrew_score
        r2 = -1 if current_time > 500 else 0
        r3 = 1 if desired_position else 0        
        return [r1, r2, r3]
    
    @override(RewardBuilder)
    def calculate_q(self, scores):
        return None

    @override(RewardBuilder)
    def get_num_rewards(self):
        return 3
