import os
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override
from rl.reward_manager import RewardManager

class PolicyMaker(TrialListener, EpisodeListener):
    def __init__(self, top_n, min_recorded_reward, milestone_episodes=[], use_num_steps_as_reward=False, save_agent=False):
        self.top_n = top_n
        self.min_recorded_reward = min_recorded_reward
        self.milestone_episodes = milestone_episodes
        self.use_num_steps_as_reward = use_num_steps_as_reward
        self.save_agent = save_agent

    @override(TrialListener)
    def before_trial(self, trial_event):
        self.reward_manager = RewardManager(self.top_n, self.min_recorded_reward)

    @override(TrialListener)
    def after_trial(self, trial_event):
        if self.save_agent:
            activity_context = trial_event.activity_context
            path = activity_context.out_path + '/agent' + str(activity_context.trial).zfill(2) + '-' + str(activity_context.num_episodes) + '.p'
            trial_event.agent.save(path)
        
    @override(EpisodeListener)
    def after_episode(self, event):
        activity_context = event.activity_context
        out_path = activity_context.out_path
        trial = activity_context.trial
        episode = activity_context.episode
        step = activity_context.step
        num_episodes = activity_context.num_episodes
        if episode == num_episodes or episode in self.milestone_episodes:
            policy_path = out_path + '/policy' + str(trial).zfill(2) + '-' + str(episode) + '.p'
            event.agent.save_policy(policy_path)
            
        reward = step if self.use_num_steps_as_reward else event.avg_reward
        added, removed = self.reward_manager.probably_add(reward, episode)
        if added is not None:
            if removed is not None:
                policy_path = out_path + '/policy' + str(trial).zfill(2) + '-' + str(removed[1]).zfill(6) + '-' + format(removed[0], '.2f') + '.p'
                if os.path.exists(policy_path):
                    os.remove(policy_path)
            policy_path = out_path + '/policy' + str(trial).zfill(2) + '-' + str(added[1]).zfill(6) + '-' + format(added[0], '.2f') + '.p'
            event.agent.save_policy(policy_path)