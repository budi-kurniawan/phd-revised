class EpisodeEvent:
    # call using 'EpisodeEvent(trial, episode, reward=1.2)' or 'EpisodeEvent(trial, episode, step=5000'
    def __init__(self, activity_context, *args, **kwargs):
        self.activity_context = activity_context
        self.reward = kwargs.get('reward', 0.0)
        self.avg_reward = kwargs.get('avg_reward', 0.0)
        self.agent = kwargs.get('agent', None)
        self.tester = kwargs.get('tester', None)
        self.env = kwargs.get('env', None)
        self.stopper = kwargs.get('stopper', None)