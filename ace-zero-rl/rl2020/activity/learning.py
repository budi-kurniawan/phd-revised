""" A class representing RL learning"""
from datetime import datetime
import os
from rl2020.event.session_event import SessionEvent
from rl2020.event.trial_event import TrialEvent
from rl2020.event.episode_event import EpisodeEvent
from rl2020.event.step_event import StepEvent
from rl2020.activity.activity import Activity
from rl2020.activity.activity_context import ActivityContext
from rl2020.agent_builder.agent_builder import AgentBuilder

class Learning(Activity):
    def learn(self, env, out_path:str, start_trial: int, num_trials: int, num_episodes: int, max_steps_per_episode: int, 
              agent_builder: AgentBuilder) -> None:
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
            self.fire_before_trial_event(TrialEvent(activity_context)) # allows a listener to change start_episode and search for a policy path
            seed = trial
            env.seed(seed)
            agent = agent_builder.load_or_create_agent(activity_context, seed)
            agent.trial_start(activity_context)
            max_reward = 0
            max_num_steps = 0
            total_steps = 0
            for episode in range(activity_context.start_episode, num_episodes + 1):
                activity_context.episode = episode
                # env.reset() and fire_before_episode_event must be reversed, just like in Testing.test()
                self.fire_before_episode_event(EpisodeEvent(activity_context, agent=agent, env=env))
                state = env.reset()
                self.fire_after_env_reset_event(EpisodeEvent(activity_context, agent=agent, env=env))
                agent.episode_start(activity_context)
                ep_reward = 0.0
                for step in range(1, max_steps_per_episode + 1):
                    activity_context.step = step
                    total_steps += 1
                    activity_context.total_steps = total_steps
                    self.fire_before_step_event(StepEvent(activity_context, env=env))
                    action = agent.select_action(state)
                    next_state, reward, terminal, env_data = env.step(action)
                    terminal = terminal or step == max_steps_per_episode # just in case the env does not set terminal, so that the agent knows
                    agent.update(activity_context, state, action, reward, next_state, terminal, env_data)
                    state = next_state
                    ep_reward += reward
                    self.fire_after_step_event(StepEvent(activity_context, env=env, reward=reward, agent=agent))
                    if terminal:
                        break
                if max_reward < ep_reward:
                    max_reward = ep_reward
                
                if max_num_steps < step:
                    max_num_steps = step
                    self.fire_max_num_steps_event(EpisodeEvent(activity_context, agent=agent, env=env))
                
                agent.episode_end(activity_context)
                self.fire_after_episode_event(EpisodeEvent(activity_context, reward=ep_reward,
                        avg_reward=(ep_reward/step), agent=agent, env=env))
            agent.trial_end(activity_context)
            trial_end_time = datetime.now()
            activity_context.trial_end_time = trial_end_time
            self.fire_after_trial_event(TrialEvent(activity_context, agent=agent, env=env))
        self.fire_after_session_event(SessionEvent(activity_context))