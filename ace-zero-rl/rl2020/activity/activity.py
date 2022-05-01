""" A base class for any activity, including learning and testing"""
from rl2020.listener.session_listener import SessionListener
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.listener.step_listener import StepListener

class Activity:

    def __init__(self):
        self.session_listeners = []
        self.trial_listeners = []
        self.episode_listeners = []
        self.step_listeners = []

    def add_listener(self, listener):
        if isinstance(listener, SessionListener):
            self.session_listeners.append(listener)
        if isinstance(listener, TrialListener):
            self.trial_listeners.append(listener)
        if isinstance(listener, EpisodeListener):
            self.episode_listeners.append(listener)
        if isinstance(listener, StepListener):
            self.step_listeners.append(listener)
     
    def fire_before_session_event(self, session_event):
        for listener in self.session_listeners:
            listener.before_session(session_event)

    def fire_after_session_event(self, session_event):
        for listener in self.session_listeners:
            listener.after_session(session_event)

    def fire_before_trial_event(self, trial_event):
        for listener in self.trial_listeners:
            listener.before_trial(trial_event)
    
    def fire_after_trial_event(self, trial_event):
        for listener in self.trial_listeners:
            listener.after_trial(trial_event)
     
    def fire_before_episode_event(self, episode_event):
        for listener in self.episode_listeners:
            listener.before_episode(episode_event)

    def fire_after_env_reset_event(self, episode_event):
        for listener in self.episode_listeners:
            listener.after_env_reset(episode_event)
            
    def fire_after_episode_event(self, episode_event):
        for listener in self.episode_listeners:
            listener.after_episode(episode_event)
     
    def fire_max_num_steps_event(self, episode_event):
        for listener in self.episode_listeners:
            listener.new_max_num_steps(episode_event)
    
    def fire_before_step_event(self, step_event):
        for listener in self.step_listeners:
            listener.before_step(step_event)

    def fire_after_step_event(self, step_event):
        for listener in self.step_listeners:
            listener.after_step(step_event)