import os
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override
from rl.reward_manager import RewardManager

class MultiObjectivePolicyMaker(TrialListener, EpisodeListener):
    def __init__(self, top_n, min_recorded_reward, num_rewards):
        self.top_n = top_n
        self.min_recorded_reward = min_recorded_reward
        self.num_rewards = num_rewards
        self.use_num_steps_as_reward = False
        self.save_agent = False

    @override(TrialListener)
    def before_trial(self, trial_event):
        self.reward_manager = RewardManager(self.top_n, self.min_recorded_reward)

    @override(TrialListener)
    def after_trial(self, event):
        if self.save_agent:
            trial = event.activity_context.trial
            num_episodes = event.activity_context.num_episodes
            out_path = event.activity_context.out_path
            path = out_path + '/agent' + str(trial).zfill(2) + '-' + str(num_episodes) + '.p'
            event.agent.save(path)
        
    @override(EpisodeListener)
    def after_episode(self, event):
        trial = event.activity_context.trial
        episode = event.activity_context.episode
        step = event.activity_context.step
        out_path = event.activity_context.out_path
        num_episodes = event.activity_context.num_episodes
        if episode == num_episodes or episode * 2 == num_episodes or episode % 100_000 == 0 or episode == 50_000:
            policy_path = out_path + '/policy' + str(trial).zfill(2) + '-' + str(episode) + '.p'
            event.agent.save_policy(policy_path)
            
        reward = step if self.use_num_steps_as_reward else event.avg_reward
        added, removed = self.reward_manager.probably_add(reward, episode)
        if added is not None:
            if removed is not None:
                for i in range(self.num_rewards):
                    policy_path = out_path + '/policy' + str(trial).zfill(2) + '-' + str(removed[1]).zfill(6) + '-' + format(removed[0], '.2f') \
                            + '.p_' + str(i)
                    if os.path.exists(policy_path):
                        os.remove(policy_path)
            policy_path = out_path + '/policy' + str(trial).zfill(2) + '-' + str(added[1]).zfill(6) + '-' + format(added[0], '.2f') + '.p'
            event.agent.save_policy(policy_path)