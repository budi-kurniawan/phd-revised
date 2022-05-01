from rl2020.listener.trial_listener import TrialListener
from rl2020.util.util import override

""" Checks if there are policy files in the given path and, if any, passes the latest policy file to the agent so that the agent may continue learning"""
class PolicyLoader(TrialListener):
    @override(TrialListener)
    def before_trial(self, event):
        from os import listdir
        from os.path import exists, isfile, join
        activity_context = event.activity_context
        out_path = activity_context.out_path
        if not exists(out_path):
            return
        trial = activity_context.trial        
        starts_with_filter = 'policy' + str(trial).zfill(2) + '-'
        files = [f for f in listdir(out_path) if isfile(join(out_path, f)) and f.startswith(starts_with_filter)]
        tuples = []
        for file in files:
            index1 = file.index('-')
            index2 = file.index('.', index1 + 1)
            if file[index1+1 : index2].find('-') != -1:
                continue # skip intermediate policy files (in the form policy00-9999-0.33.p)
            episode = int(file[index1 + 1 : index2])
            tuples.append((episode, file))
        tuples = sorted(tuples, reverse = True)
        if len(tuples) == 0:
            return
        last_episode = tuples[0][0]
        policy_path = out_path + '/' + str(tuples[0][1])
        print('Loaded policy', policy_path)
        print('Starting from episode:', last_episode + 1)
        activity_context.start_episode = last_episode + 1
        activity_context.initial_policy_path = policy_path