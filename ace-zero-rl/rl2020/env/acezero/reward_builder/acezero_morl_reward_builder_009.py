from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

class AceZeroMORLRewardBuilder009(RewardBuilder):
    @override(RewardBuilder)
    def get_rewards(self, data):
        viper = data.get('viper', None)
        return [viper.mcgrew_range, viper.mcgrew_angle]
    
    @override(RewardBuilder)
    def calculate_q(self, scores):
        return None

    @override(RewardBuilder)
    def get_num_rewards(self):
        return 2
