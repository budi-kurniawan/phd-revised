import pickle
from rl2020.activity.activity_context import ActivityContext

class AgentBuilder():
    
    def __init__(self, num_actions: int, *args, **kwargs) -> None:
        self.num_actions = num_actions
        self.discretizer = kwargs.get('discretizer', None)
        self.normalizer = kwargs.get('normalizer', None)
        self.reward_builder = kwargs.get('reward_builder', None)
        self.agent_load_path = kwargs.get('agent_load_path', None)
        self.always_create = kwargs.get('always_create', False)
        
    def load_or_create_agent(self, activity_context, seed):
        if self.always_create or self.agent_load_path is None:
            return self.create_agent(seed, activity_context.initial_policy_path)
        else:
            agent = self.load_agent(activity_context, seed)
            if agent is None:
                agent = self.create_agent(seed, activity_context.initial_policy_path)
            return agent
    
    def load_agent(self, activity_context, seed):
        from os import listdir
        from os.path import exists, isfile, join
        if not exists(self.agent_load_path):
            return None
        trial = seed
        starts_with_filter = 'agent' + str(trial).zfill(2) + '-'
        # agent filename in the format agent[xx]-[yyyyyy].p, where xx = trial and yyyyyy = num_episodes
        files = [f for f in listdir(self.agent_load_path) if isfile(join(self.agent_load_path, f)) and f.startswith(starts_with_filter)]
        tuples = []
        for file in files:
            index1 = file.index('-')
            index2 = file.index('.', index1 + 1)
            episode = int(file[index1 + 1 : index2])
            tuples.append((episode, file))
        tuples = sorted(tuples, reverse = True)
        if len(tuples) == 0:
            return None
        last_episode = tuples[0][0]
        agent_path = self.agent_load_path + '/' + str(tuples[0][1])
        print('load agent from ' + agent_path)
        file = open(agent_path,'rb')
        agent = pickle.load(file)
        file.close()
        activity_context.start_episode = last_episode + 1
        print("start episode:", activity_context.start_episode)
        return agent

    def create_agent(self, seed, initial_policy_path):
        pass