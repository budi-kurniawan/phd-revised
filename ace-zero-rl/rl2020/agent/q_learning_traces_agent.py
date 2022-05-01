from rl2020.util.util import override
from rl2020.agent.q_learning_agent import QLearningAgent
import numpy as np
from rl2020.activity.activity_context import ActivityContext

__author__ = 'bkurniawan'

"""
This class represents an Q-learning with traces agent, using replacing traces (instead of accumulating traces)
As such, e[s][a] is set to 1, instead of e[s][a] *= increment. Therefore, we do not need another 2-dimensional array
Rather, we'll use visited to make the code faster

This algorithm is called Watkin's Q(lambda) (Q-learning + eligibility traces) and can be found in
    https://stackoverflow.com/questions/40862578/how-to-understand-watkinss-q%CE%BB-learning-algorithm-in-suttonbartos-rl-book
    
Do not use http://www-anw.cs.umass.edu/~barto/courses/cs687/Chapter%207.pdf (wrong)
"""
class QLearningTracesAgent(QLearningAgent):
    def __init__(self, num_actions: int, discretizer, seed=None, initial_policy_path=None):
        super().__init__(num_actions, discretizer, seed, initial_policy_path)
        self.e = np.zeros([self.num_states, num_actions], dtype=np.float64)
        self.visited = []

    @override(QLearningAgent)
    def episode_start(self, activity_context: ActivityContext)->None:
        super().episode_start(activity_context)
        self.__reset_traces()

    @override(QLearningAgent)
    def update(self, activity_context, state, action, reward, next_state, terminal, env_data) -> None:
        # this is a better implementation than the one in Sutton's book (1st edition) because you don't need to
        # calculate a' (next action)
        discrete_state = self.discretizer.discretize(state)
        next_discrete_state = self.discretizer.discretize(next_state)
        q = self.q
        next_max = np.max(q[next_discrete_state])
        delta = reward + QLearningAgent.GAMMA * next_max - q[discrete_state][action]
        q[discrete_state][action] += QLearningAgent.ALPHA * delta

        # we want to know if action was obtained by exploration or exploitation
        exploit = q[discrete_state][action] == np.max(q[discrete_state])
        if exploit:
            e = self.e
            for s, a in self.visited:
                q[s][a] += QLearningAgent.ALPHA * delta * e[s][a]
                e[s][a] *= self.GAMMA * self.LAMBDA
            e[discrete_state][action] = 1
            if (discrete_state, action) not in self.visited:
                self.visited.append((discrete_state, action)) # record visited state/action pairs so we don't have to update state/actions that were never visited
        else:
            self.__reset_traces()

    def __reset_traces(self):
        e = self.e
        for s, a in self.visited:
            e[s][a] = 0.0
        del self.visited[:]
