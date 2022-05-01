from d2dspl_train import *
import d2dspl_train as base
import rl
from rl.agent2.qlearning_agent import QLearningAgent
from rl.env.ace_zero_env import AceZeroEnvironment

def create_agent(num_states, num_actions):
    print("creating QL Agent")
    return QLearningAgent(num_states, num_actions)

base.create_agent = create_agent

if __name__ == '__main__':
    scenario_name = 'standard-001.json'
    out_path = 'rl_results/ql-d2dspl-001.json'
    num_trials = 10
    base.NUM_EPISODES = 20_000
    base.MAX_NUM_SAMPLES_FOR_CLASSIFIER = 150
    start_trial = 0
    run(scenario_name, out_path, num_trials, start_trial)