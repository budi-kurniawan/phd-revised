class TesterBuilder():
    
    def __init__(self, policy_path: str, **kwargs) -> None:
        self.policy_path = policy_path
        self.discretizer = kwargs.get('discretizer', None)
        self.normalizer = kwargs.get('normalizer', None)
        
    def create_tester(self, trial: int):
        pass
