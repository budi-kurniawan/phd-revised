from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

class AceZeroMORLRewardBuilder010(RewardBuilder):
    @override(RewardBuilder)
    def get_rewards(self, data):
        viper = data.get('viper', None)
        delta_v = min(100, abs(viper.delta_v))
        delta_v_score = (1.0 - delta_v/100.0)
        return [viper.mcgrew_range, delta_v_score]
    
    @override(RewardBuilder)
    def calculate_q(self, scores):
        return None

    @override(RewardBuilder)
    def get_num_rewards(self):
        return 2
