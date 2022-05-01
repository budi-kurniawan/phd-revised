from rl2020.morl.reward_builder import RewardBuilder
from rl2020.util.util import override

class AceZeroEnvironmentRewardBuilder101(RewardBuilder):
    def __init__(self):
        self.reset()
        
    @override(RewardBuilder)
    def get_reward(self, data):
        viper = data.get('viper', None)
        r = viper.contact_range
        aa = viper.contact_aa
        ata = viper.contact_ata
        
        desired_position = r > 152 and r < 914 and abs(aa) < 30 and abs(ata) < 30
        self.t = self.t + 1 if desired_position else 0
        if self.t == 10: # goal reached
            self.terminal = True
        return viper.mcgrew_score

    @override(RewardBuilder)
    def calculate_q(self, scores):
        return None

    @override(RewardBuilder)
    def get_num_rewards(self):
        return 3

    @override(RewardBuilder)
    def is_terminal(self):
        return self.terminal

    @override(RewardBuilder)
    def reset(self):
        self.terminal = False
        self.t = 0
