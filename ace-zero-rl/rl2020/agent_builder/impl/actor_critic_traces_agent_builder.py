from rl2020.util.util import override
from rl2020.agent_builder.agent_builder import AgentBuilder
from rl2020.agent.actor_critic_traces_agent import ActorCriticTracesAgent

class ActorCriticTracesAgentBuilder(AgentBuilder):
    @override(AgentBuilder)
    def create_agent(self, seed, initial_policy_path):
        return ActorCriticTracesAgent(self.num_actions, self.discretizer, seed, initial_policy_path)        
    