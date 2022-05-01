from rl2020.activity.activity_context import ActivityContext

class StepEvent:
    def __init__(self, activity_context: ActivityContext, *args, **kwargs) -> None:
        self.activity_context = activity_context
        self.env = kwargs.get('env', None)
        self.reward = kwargs.get('reward', None)
        self.agent = kwargs.get('agent', None)
        self.state = kwargs.get('state', None)
        self.action = kwargs.get('action', None)
        self.env_data = kwargs.get('env_data', None)
