from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override
from rl2020.listener.step_listener import StepListener
from rl2020.listener.impl.console_log_listener import ConsoleLogListener
from rl2020.listener.impl.file_log_listener import FileLogListener, RewardType
from rl2020.listener.impl.policy_maker import PolicyMaker

class BasicFunctions(TrialListener, EpisodeListener, StepListener):
    def __init__(self, **kwargs):
        self.reward_type = kwargs.get('reward_type', RewardType.AVERAGE)
        self.chart_offset = kwargs.get('chart_offset', 0)
        self.top_n = kwargs.get('top_n', 10)
        self.min_recorded_reward = kwargs.get('min_recorded_reward', 0.1)
        self.milestone_episodes = kwargs.get('milestone_episodes', [])
        self.use_num_steps_as_reward = kwargs.get('use_num_steps_as_reward', False)
        self.save_agent = kwargs.get('save_agent', False)
        
        self.console_log_listener = ConsoleLogListener()
        self.file_log_listener = FileLogListener(self.chart_offset, self.reward_type)
        self.policy_maker = PolicyMaker(self.top_n, self.min_recorded_reward, self.use_num_steps_as_reward, self.save_agent)

    @override(TrialListener)
    def before_trial(self, event):
        self.file_log_listener.before_trial(event)
        self.policy_maker.before_trial(event)

    @override(TrialListener)
    def after_trial(self, event):
        self.console_log_listener.after_trial(event)
        self.file_log_listener.after_trial(event)
        self.policy_maker.after_trial(event)

    @override(EpisodeListener)
    def before_episode(self, event):
        pass
    
    @override(EpisodeListener)
    def after_episode(self, event):
        self.console_log_listener.after_episode(event)
        self.file_log_listener.after_episode(event)
        self.policy_maker.after_episode(event)