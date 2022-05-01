from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override
import numpy as np

class AceZeroMORLRewardBuilder012(RewardBuilder):
    @override(RewardBuilder)
    def get_rewards(self, data):
        viper = data.get('viper', None)
        r = viper.contact_range
        aa = viper.contact_aa
        ata = viper.contact_ata
        range_score = -1 if r < 900 and np.abs(aa) > 150 else 0
        return [viper.mcgrew_score, range_score]
    
    @override(RewardBuilder)
    def calculate_q(self, scores):
        return None

    @override(RewardBuilder)
    def get_num_rewards(self):
        return 2
