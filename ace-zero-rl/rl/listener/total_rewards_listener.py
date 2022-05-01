from rl.listener.learning_listener import LearningListener

class TotalRewardsListener(LearningListener):
    def __init__(self, context):
        super(TotalRewardsListener, self).__init__(context)
        
    def trial_start(self):
        total_reward_path = self.context.result_parent_path / 'total_reward.txt'
        total_reward_file = open(total_reward_path, 'w')
        total_reward_file.write('Episode,Total Reward\n')
        self.total_reward_file = total_reward_file
        
    def trial_end(self):
        self.total_reward_file.close()
    
    def episode_end(self):
        context = self.context
        self.total_reward_file.write(str(context.episode) + ',' + str(context.total_reward) + '\n')
