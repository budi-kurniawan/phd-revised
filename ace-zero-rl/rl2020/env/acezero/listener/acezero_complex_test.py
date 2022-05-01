from rl2020.listener.step_listener import StepListener
from rl2020.util.util import override
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.listener.impl.seedable_trial_listener import SeedableTrialListener
from rl2020.listener.trial_listener import TrialListener

class AceZeroComplexTest(SeedableTrialListener, StepListener, EpisodeListener):
    """ Uses different scenarios for each 'episode'."""
    @override(TrialListener)
    def before_trial(self, event):
        super().before_trial(event)
        self.scenarios = []
        for i in range(1, 4 + 1):
            scenario = 'complex-00' + str(i) + '.json'
            self.scenarios.append(scenario)
        
    @override(EpisodeListener)
    def before_episode(self, event):
        env = event.env
        episode = event.activity_context.episode
        scenario = self.scenarios[episode - 1]
        print('episode:', episode, ', scenario:', scenario)
        env.change_scenario(scenario)

    @override(EpisodeListener)
    def after_episode(self, event):
        if event.activity_context.episode == len(self.scenarios):
            event.stopper.active = True