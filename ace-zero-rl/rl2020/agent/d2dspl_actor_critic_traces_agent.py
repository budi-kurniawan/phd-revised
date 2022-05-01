""" A class representing D2D-SPL Actor-Critic with traces agents """
import numpy as np
import pickle
from datetime import datetime
from sklearn.neural_network import MLPClassifier
from rl2020.util.util import override
from rl2020.activity.activity_context import ActivityContext
from rl2020.agent.actor_critic_traces_agent import ActorCriticTracesAgent
from rl2020.agent.seedable_agent import SeedableAgent

__author__ = 'bkurniawan'

class D2DSPLActorCriticTracesAgent(SeedableAgent):
    
    def __init__(self, num_actions: int, discretizer, max_num_samples_for_classifier, normalizer, milestone_episodes, hidden_layer_sizes, seed):
        super().__init__(seed)
        self.max_num_samples_for_classifier = max_num_samples_for_classifier
        self.buffer_trim_interval = 5_000
        self.normalizer = normalizer
        self.hidden_layer_sizes = hidden_layer_sizes
        self.milestone_episodes = milestone_episodes
        self.solver = 'lbfgs'
        self.alpha = 0.0001
        self.max_num_records = 14_000
        self.time_spent_on_creating_classifiers = 0
        self.discretizer = discretizer
        self.buffer = []
        self.base_agent = ActorCriticTracesAgent(num_actions, discretizer, seed, None)

    @override(ActorCriticTracesAgent)
    def episode_start(self, activity_context: ActivityContext) -> None:
        # reset traces
        self.base_agent.episode_start(activity_context)
        num_discrete_states = self.discretizer.get_num_discrete_states()
        num_state_variables = self.discretizer.get_num_state_variables()
        self.state_stats = np.zeros([num_discrete_states, num_state_variables], dtype=np.float64)
        self.state_visits = np.zeros(num_discrete_states, dtype=np.int32)
        self.next_state_stats = np.zeros([num_discrete_states, num_state_variables], dtype=np.float64)
        self.reward_stats = np.zeros(num_discrete_states, dtype=np.float32)
        self.episode = activity_context.episode
        self.ep_reward = 0

    @override(SeedableAgent)
    def episode_end(self, activity_context: ActivityContext) -> None:
        episode = activity_context.episode
        buffer = self.buffer
        buffer.append((episode, self.ep_reward, self.state_stats, self.state_visits, self.next_state_stats, self.reward_stats))
        if episode % self.buffer_trim_interval == 0:
            print('trim buffer at episode ', episode)
            buffer.sort(key=lambda tup: tup[1], reverse=True) # sorted by ep_reward, biggest on top
            del buffer[self.max_num_samples_for_classifier : ] # keep the first n samples with the highest ep_rewards
        if episode in self.milestone_episodes:
            if len(buffer) > self.max_num_samples_for_classifier:
                print('trim buffer before saving it')
                buffer.sort(key=lambda tup: tup[1], reverse=True) # sorted by ep_reward, biggest on top
                del buffer[self.max_num_samples_for_classifier : ] # keep the first n samples with the highest ep_rewards            
            out_path = activity_context.out_path
            trial = activity_context.trial
            buffer_path = out_path + '/d2dspl-buffer-' + str(trial).zfill(2) + '-' + str(episode).zfill(8) + '.p'
            # not saving buffer as it is too big (2GB)
#             pickle.dump(buffer, open(buffer_path, "wb"))
            normalized_training_set = self.create_training_set(trial, episode, out_path)
            print('creating classifier learning for buffer ', buffer_path)
            start_time = datetime.now()
            self.create_classifier(trial, episode, out_path, normalized_training_set)            
            end_time = datetime.now()
            num_seconds = (end_time - start_time).total_seconds()
            self.time_spent_on_creating_classifiers += num_seconds
            self.write_to_learning_times_file(out_path, 'Creating classifier ' + buffer_path + ' took ' + str(num_seconds) + ' seconds')
        
    @override(ActorCriticTracesAgent)
    def update(self, activity_context, state, action, reward, next_state, terminal, env_data) -> None:
        self.base_agent.update(activity_context, state, action, reward, next_state, terminal, env_data)
        self.ep_reward += reward
        discrete_state = self.discretizer.discretize(state)
        self.state_visits[discrete_state] += 1
        self.state_stats[discrete_state] += state
        self.next_state_stats[discrete_state] += next_state
        self.reward_stats[discrete_state] += reward

    def select_action(self, state) -> int:
        return self.base_agent.select_action(state)

    @override(ActorCriticTracesAgent)
    def trial_end(self, activity_context: ActivityContext):
        trial = activity_context.trial
        trial_end_time = datetime.now()
        trial_duration_in_seconds = (trial_end_time - activity_context.trial_start_time).total_seconds()
        msg = 'Trial ' + str(trial) + ' took ' + str(trial_duration_in_seconds) + ' seconds, ' + \
                'including ' + str(self.time_spent_on_creating_classifiers) + ' seconds for training all classifiers'
        self.write_to_learning_times_file(activity_context.out_path, msg)
        del self.buffer

    def create_training_set(self, trial, episode, out_path):
        normalized_training_set = []
        num_discrete_states = self.discretizer.get_num_discrete_states()
        num_state_variables = self.discretizer.get_num_state_variables()
        # consolidated_next_state_stats and consolidated_rewards are not used in D2D-SPL, but are useful in other methods such as hybrid D2D-DDQN
        consolidated_state_stats = np.zeros([num_discrete_states, num_state_variables], dtype=np.float64)
        consolidated_state_visits = np.zeros(num_discrete_states, dtype=np.int32)
        consolidated_next_state_stats = np.zeros([num_discrete_states, num_state_variables], dtype=np.float64)
        consolidated_rewards = np.zeros(num_discrete_states, dtype=np.float32)
        buffer = self.buffer
        theta = self.base_agent.theta
        for i in range(len(buffer)):
            # buffer contains results for top episodes
            # ep_reward is the average reward for the episode, reward is a list of all rewards in all timesteps, group by discrete states
            ep, ep_reward, state_stats, state_visits, next_state_stats, reward = buffer[i]
            consolidated_state_stats += state_stats
            consolidated_state_visits += state_visits
            consolidated_next_state_stats += next_state_stats
            consolidated_rewards += reward
        normalized_training_set_path = out_path + '/d2dspl-normalised_training_set-' + str(trial).zfill(2) + '-' + str(episode).zfill(8) + '.txt'
        file = open(normalized_training_set_path, 'w') # create training_set file for D2D-SQL
        num_rows = 0
        for i in range(num_discrete_states):
            if consolidated_state_visits[i] != 0:
                consolidated_state_stats[i] /= consolidated_state_visits[i]
                consolidated_next_state_stats[i] /= consolidated_state_visits[i]
                consolidated_rewards[i] /= consolidated_state_visits[i]
                normalized_consolidated_state_stats = self.normalizer.normalize(consolidated_state_stats[i])
                normalized_consolidated_next_state_stats = self.normalizer.normalize(consolidated_next_state_stats[i])                
                s1 = np.array2string(normalized_consolidated_state_stats, separator=',', precision=4)
                s2 = np.array2string(theta[i], separator=',', precision=4)
                s3 = np.array2string(normalized_consolidated_next_state_stats, separator=',', precision=4)
                s4 = np.array2string(consolidated_rewards[i], separator=',', precision=4)
                file.write(str(i) + ',' + s1 + ',' + s2 + ',' + s3 + ',' + s4 + '\n')
                y = np.argmax(theta[i])
                normalized_training_set.append((normalized_consolidated_state_stats, y))
                num_rows += 1
        #file.close()
        print('training set created with ' + str(num_rows) + ', rows.')
        return normalized_training_set

    def create_classifier(self, trial, episode, out_path, normalized_training_set):
        classifier_path = out_path + '/d2dspl-classifier-' + str(trial).zfill(2) + '-' + str(episode).zfill(8) + '.p'
        xy = zip(*normalized_training_set)
        X = next(xy)
        Y = next(xy)
        classifier = MLPClassifier(solver=self.solver, alpha=self.alpha, random_state=1, max_iter=1_000_000, hidden_layer_sizes=self.hidden_layer_sizes).fit(X, Y)
        pickle.dump(classifier, open(classifier_path, "wb"))
        score = classifier.score(X, Y)
        print('classifier score for classifier ' + classifier_path + ' : ' + str(score))
    
    def write_to_learning_times_file(self, out_path, message):
        learning_times_file = open(out_path + '/d2dspl-agent-learning-times.txt', 'a+')
        learning_times_file.write(message + '\n')        
        learning_times_file.close()