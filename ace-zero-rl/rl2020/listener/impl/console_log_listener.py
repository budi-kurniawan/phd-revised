from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override

class ConsoleLogListener(TrialListener, EpisodeListener):
    def __init__(self):
        self.max_num_steps = 0

    @override(EpisodeListener)
    def after_episode(self, event):
        activity_context = event.activity_context
        trial = activity_context.trial
        episode = activity_context.episode
        step = activity_context.step
        print("Trial " + str(trial) + " episode " + str(episode) + ", reward:" + str(event.reward)
              + ", avg reward:" + str(event.avg_reward)
              + ", steps:" + str(step) + " (max " + str(self.max_num_steps) + ")")

    @override(TrialListener)
    def after_trial(self, event):
        ac = event.activity_context
        duration_in_seconds = (ac.trial_end_time - ac.trial_start_time).total_seconds()
        print("Trial " + str(ac.trial) + " completed in " + str(duration_in_seconds) + " seconds.")
    
    @override(EpisodeListener)
    def new_max_num_steps(self, event):
        self.max_num_steps = event.activity_context.step