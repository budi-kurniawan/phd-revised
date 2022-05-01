from . import rl_utils
import os
import pickle
import time
from pathlib import Path

class Context:
    def __init__(self, root_path=None, scenario_path=None):
        pass
    
    def init(self):
        self.e = {}
        self.e.fromkeys(range(1000000))
        self.q = {}
        self.q.fromkeys(range(400))
        
    def save_q(self, out_path=None, scenario_path=None, random_seed=None):
        self.scenario_path = scenario_path
        self.qfile_path = self.get_qfile_path(out_path, scenario_path, random_seed)
        parent_dir = Path(self.qfile_path).parent
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        self.sorted_qfile_path = parent_dir / Path('sorted-q-' + str(random_seed) + '.txt')
        # save q and sorted_q 
        with open(self.qfile_path, 'wb') as handle:
            pickle.dump(self.q, handle, protocol=pickle.HIGHEST_PROTOCOL)
        f = open(self.sorted_qfile_path, 'w')
        rl_utils.print_q(self.q, f) #action_length is assumed to be <40
        f.close()
    
    def get_qfile_path(self, out_path, scenario_path, random_seed):
        scenario_file = os.path.basename(scenario_path)
        output_path = out_path / Path(scenario_file + "/" + str(self.num_episodes).zfill(8) \
                + "-" + str(rl_utils.MIN_NUM_IN_GOAL).zfill(4))
        return output_path / Path('Q-' + str(random_seed))
        