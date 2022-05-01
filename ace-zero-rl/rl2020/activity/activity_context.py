class ActivityContext(object):
    def __init__(self, start_episode=1):
        self.start_episode = start_episode
        self.num_episodes = None
        self.initial_policy_path = None
        self.out_path = None
        self.trial = None
        self.episode = None
        self.step = None
        self.trial_start_time = None
        self.trial_end_time = None
        self.total_steps = None