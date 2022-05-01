from rl2020.util.util import override
from rl2020.agent_builder.agent_builder import AgentBuilder
from rl2020.agent.mo_actor_critic_traces_agent import MultiObjectiveActorCriticTracesAgent

class MultiObjectiveActorCriticTracesAgentBuilder(AgentBuilder):
    @override(AgentBuilder)
    def create_agent(self, seed, initial_policy_path):
        return MultiObjectiveActorCriticTracesAgent(self.num_actions, self.discretizer, self.reward_builder, seed)
