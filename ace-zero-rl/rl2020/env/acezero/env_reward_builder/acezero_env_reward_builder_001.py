import numpy as np
from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

class AceZeroEnvironmentRewardBuilder001(RewardBuilder):
    @override(RewardBuilder)
    def get_reward(self, data):
        viper = data.get('viper', None)
        ata = viper.contact_ata
        ata_score = (1.0 - np.abs(ata) / 180.0) - 0.5
        return ata_score