from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

class AceZeroEnvironmentRewardBuilder003(RewardBuilder):
    @override(RewardBuilder)
    def get_reward(self, data):
        viper = data.get('viper', None)
        contact_range = viper.contact_range
        aa = viper.contact_aa
        ata = viper.contact_ata
        abs_aa = abs(aa)
        abs_ata = abs(ata)
        head_on = abs_aa > 135 and abs_ata < 45 and contact_range < 1250
        reward = -1 if head_on else (viper.mcgrew_score + (180 - abs(aa))/1800 + (180-abs(ata))/1800 - 0.5)
        return reward