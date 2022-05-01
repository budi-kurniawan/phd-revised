from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

""" use Blue and Red's mcgrew scores"""
class AceZeroMORLRewardBuilder015(RewardBuilder):
    @override(RewardBuilder)
    def get_rewards(self, data):
        viper = data.get('viper', None)
        cobra = data.get('cobra', None)
        return [0.75 * viper.mcgrew_score, -0.25 * cobra.mcgrew_score]
    
    @override(RewardBuilder)
    def calculate_q(self, scores):
        return None

    @override(RewardBuilder)
    def get_num_rewards(self):
        return 2
