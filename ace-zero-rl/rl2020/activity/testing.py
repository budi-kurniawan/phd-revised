""" A BaseTesting is a test session"""
import os
from datetime import datetime
from rl2020.event.session_event import SessionEvent
from rl2020.event.trial_event import TrialEvent
from rl2020.event.episode_event import EpisodeEvent
from rl2020.event.step_event import StepEvent
from rl2020.util.stopper import Stopper
from rl2020.activity.activity_context import ActivityContext
from rl2020.activity.activity import Activity

class Testing(Activity):
    
    #def test(self, env, tester_builder: TesterBuilder, start_trial: int, num_trials: int, num_episodes: int, num_steps: int) -> None:
    def test(self, env, out_path, *args, **kwargs) -> None:
        start_trial = kwargs.get('start_trial', 1)
        num_trials = kwargs.get('num_trials', 1)
        num_episodes = kwargs.get('num_episodes', 1)
        max_steps_per_episode = kwargs.get('num_steps', None)
        start_episode = kwargs.get('start_episode', 1)
        tester = kwargs.get('tester', None)
        tester_builder = kwargs.get('tester_builder', None)
        if tester is not None and tester_builder is not None:
            print('Both tester and tester_builder are present. tester will be ignored')

        if not os.path.exists(out_path):
            os.makedirs(out_path)
            print('Created ' + out_path)

        end_trial = start_trial + num_trials
        activity_context = ActivityContext()
        activity_context.out_path = out_path
        activity_context.num_episodes = num_episodes
        self.fire_before_session_event(SessionEvent(activity_context))
        for trial in range(start_trial, end_trial):
            trial_start_time = datetime.now()
            activity_context.trial = trial
            activity_context.trial_start_time = trial_start_time
            activity_context.trial_end_time = None
            self.fire_before_trial_event(TrialEvent(activity_context))
            seed = trial
            env.seed(seed)
            if tester_builder is not None:
                tester = tester_builder.create_tester(trial)
            tester.trial_start(activity_context)
            max_reward = 0
            max_num_steps = 0
            for episode in range(start_episode, start_episode + num_episodes):
                activity_context.episode = episode
                stopper = Stopper()
                self.fire_before_episode_event(EpisodeEvent(activity_context, tester=tester, env=env, stopper=stopper))
                state = env.reset()
                self.fire_after_env_reset_event(EpisodeEvent(activity_context, tester=tester, env=env, stopper=stopper))
                tester.episode_start(activity_context)
                ep_reward = 0.0
                for step in range(1, max_steps_per_episode + 1):
                    activity_context.step = step
                    self.fire_before_step_event(StepEvent(activity_context, env=env))
                    action = tester.select_action(state)
                    next_state, reward, terminal, env_data = env.step(action)
                    state = next_state
                    ep_reward += reward
                    self.fire_after_step_event(StepEvent(activity_context, env=env, reward=reward, 
                                                         state=state, action=action, env_data=env_data))
                    if terminal:
                        break
                if max_reward < ep_reward:
                    max_reward = ep_reward
                
                if max_num_steps < step:
                    max_num_steps = step
                    self.fire_max_num_steps_event(EpisodeEvent(activity_context))
                
                self.fire_after_episode_event(EpisodeEvent(activity_context, reward=ep_reward,
                        avg_reward=(ep_reward/step), tester=tester, env=env, stopper=stopper))
                tester.episode_end(activity_context)
                if stopper.active:
                    break
            tester.trial_end(activity_context)
            trial_end_time = datetime.now()
            activity_context.trial_end_time = trial_end_time
            self.fire_after_trial_event(TrialEvent(activity_context, trial_start_time=trial_start_time, trial_end_time=trial_end_time))
        self.fire_after_session_event(SessionEvent(activity_context))