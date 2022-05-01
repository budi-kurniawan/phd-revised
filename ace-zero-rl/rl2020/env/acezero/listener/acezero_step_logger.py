import os
from rl2020.listener.step_listener import StepListener
from rl2020.util.util import override
from rl2020.listener.episode_listener import EpisodeListener

class AceZeroStepLogger(StepListener, EpisodeListener):
    @override(EpisodeListener)
    def before_episode(self, event):
        activity_context = event.activity_context
        trial = activity_context.trial
        episode = activity_context.episode
        out_path = activity_context.out_path
        if episode == 1 or episode == 79:
            self.log_file = open(out_path + '/steplog-' + str(trial).zfill(2) + '-' + str(episode).zfill(6) + '.txt', 'w')
        else:
            self.log_file = None

    @override(EpisodeListener)
    def after_episode(self, event):
        if self.log_file is not None:
            self.log_file.close()

    @override(StepListener)
    def after_step(self, event):
        if self.log_file is None:
            return
        step = event.activity_context.step
        viper_action = event.action
        viper_state = event.state
        env_data = event.env_data
        cobra_action = env_data['cobra_action']
        cobra_state = env_data['cobra_state']
        self.log_file.write(str(step) + ': ' + str(viper_action) + ',' + str(viper_state) + '\t\t' 
                            + str(cobra_action) + ',' + str(cobra_state) + '\n')