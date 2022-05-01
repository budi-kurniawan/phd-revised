from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

class AceZeroMORLRewardBuilder008(RewardBuilder):
    @override(RewardBuilder)
    def get_rewards(self, data):
        viper = data.get('viper', None)
#         r = viper.contact_range
        aa = viper.contact_aa
        ata = viper.contact_ata
# 
#         rd = 380 # desired range
#         k = 5 # constant measured in metres/degree
#         range_score = np.exp(-np.abs(r-rd)/(180.0*k))
#         aa_score = (1.0 - np.abs(aa)/180.0)
#         ata_score = (1.0 - np.abs(ata)/180.0)
        return [viper.mcgrew_score, (180 - abs(aa))/180 , (180-abs(ata))/180]
    
    @override(RewardBuilder)
    def calculate_q(self, scores):
        return None

    @override(RewardBuilder)
    def get_num_rewards(self):
        return 3
