from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

class AceZeroEnvironmentRewardBuilder002(RewardBuilder):
    @override(RewardBuilder)
    def get_reward(self, data):
        viper = data.get('viper', None)
        aa = viper.contact_aa
        ata = viper.contact_ata
        reward = viper.mcgrew_score + (180 - abs(aa))/1800 + (180-abs(ata))/1800 - 0.5
        return reward