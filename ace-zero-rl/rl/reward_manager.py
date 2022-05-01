"""
    RewardManager manages top X (reward, episode) tuples
"""
class RewardManager():
    def __init__(self, num_models = 5, min_reward = 0.2) -> None:
        self.num_models = num_models
        self.min_reward = min_reward
        self.list = []

    # adds a (reward, episode) if reward > threshold and return (added, removed)
    def probably_add(self, reward: float, episode: int):
        if reward < self.min_reward:
            return None, None
        candidate = (reward, episode)
        if len(self.list) < self.num_models:
            self.list.append(candidate)
            return candidate, None
        else:
            minimum_reward = self.get_minimum_reward()
            if minimum_reward is None or reward <= minimum_reward:
                return None, None
            else:
                removed = self.remove_value_with_minimum_reward()
                self.list.append(candidate)
                return candidate, removed
                
            
    def get_minimum_reward(self):
        if len(self.list) == 0:
            return None
        return sorted(self.list)[0][0]
        
    def remove_value_with_minimum_reward(self):
        if len(self.list) == self.num_models:
            pair_to_remove = sorted(self.list)[0]
            self.list.remove(pair_to_remove)
            return pair_to_remove
        else:
            return None

if __name__ == '__main__':
    rewardManager = RewardManager(5, 0.2)
    rewardManager.probably_add(0.5, 1)
    rewardManager.probably_add(0.3, 2)
    rewardManager.probably_add(0.2, 4)
    rewardManager.probably_add(0.7, 5)
    added, removed = rewardManager.probably_add(0.9, 6)
    print('added:', added, ', removed:', removed)
    print(rewardManager.list)
    print('min reward:', rewardManager.get_minimum_reward())
    
    added, removed = rewardManager.probably_add(0.25, 7)
    print('added:', added, ', removed:', removed)
    print(rewardManager.list)
    print('min reward:', rewardManager.get_minimum_reward())

    added, removed = rewardManager.probably_add(1.25, 8)
    print('added:', added, ', removed:', removed)
    print(rewardManager.list)
    print('min reward:', rewardManager.get_minimum_reward())
