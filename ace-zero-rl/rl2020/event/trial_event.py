class TrialEvent:
    def __init__(self, activity_context, *args, **kwargs):
        self.activity_context = activity_context
        self.agent = kwargs.get('agent', None)
        self.env = kwargs.get('env', None)