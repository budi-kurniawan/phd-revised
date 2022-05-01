""" A RewardBuilder constructs rewards for MORL agents. Used in DQNMultiObjectiveAgent """
class RewardBuilder:
    def get_reward(self, data):
        return None
    
    def get_rewards(self, data):
        return []
    
    def calculate_q(self, scores):
        return None
    
    def get_num_rewards(self):
        return 0

    def is_terminal(self):
        return False

    def reset(self):
        pass
