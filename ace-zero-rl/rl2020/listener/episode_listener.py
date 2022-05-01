from rl2020.listener.listener import Listener

class EpisodeListener(Listener):
    def before_episode(self, episode_event):
        pass

    def after_env_reset(self, episode_event):
        pass

    def after_episode(self, episode_event):
        pass
    
    def new_max_num_steps(self, episode_event):
        pass