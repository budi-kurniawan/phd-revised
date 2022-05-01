from rl2020.util.util import override
from rl2020.agent_builder.agent_builder import AgentBuilder
from rl2020.agent.random_agent import RandomAgent

class RandomAgentBuilder(AgentBuilder):
    @override(AgentBuilder)
    def create_agent(self, seed):
        return RandomAgent(self.num_actions, seed)