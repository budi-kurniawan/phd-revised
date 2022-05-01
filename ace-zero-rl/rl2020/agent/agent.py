""" A class representing RL agents """
import pickle
from rl2020.activity.activity_context import ActivityContext

__author__ = 'Budi Kurniawan'

class Agent:
    # called at the beginning of a trial
    def trial_start(self, activity_context: ActivityContext) -> None:
        pass

    # called at the end of a trial
    def trial_end(self, activity_context: ActivityContext) -> None:
        pass

    # called at the beginning of an episode
    def episode_start(self, activity_context: ActivityContext) -> None:
        pass    

    # called at the end of an episode
    def episode_end(self, activity_context: ActivityContext) -> None:
        pass

    def select_action(self, state) -> int:
        pass
    
    def update(self, activity_context, state, action, reward, next_state, terminal, env_data=None) -> None:
        pass
    
    def save_policy(self, path) -> None:
        pass
        
    def seed(self, seed) -> None:
        pass
    
    def save(self, path): # save this agent
        file = open(path, 'wb')
        pickle.dump(self, file)
        file.close()