from rl2020.util.util import override
from rl2020.agent_builder.agent_builder import AgentBuilder
from rl2020.agent.d2dspl_actor_critic_traces_agent import D2DSPLActorCriticTracesAgent
from rl2020.discretizer.discretizer import Discretizer
from rl2020.normalizer.normalizer import Normalizer

class D2DSPLActorCriticTracesAgentBuilder(AgentBuilder):
    
    def __init__(self, num_actions: int, discretizer: Discretizer, max_num_samples_for_classifier: int, normalizer: Normalizer,
            milestone_episodes, hidden_layer_sizes = [300, 300]) -> None:
        super().__init__(num_actions, discretizer=discretizer, normalizer=normalizer)
        self.max_num_samples_for_classifier = max_num_samples_for_classifier
        self.hidden_layer_sizes = hidden_layer_sizes
        self.milestone_episodes = milestone_episodes

    @override(AgentBuilder)
    def create_agent(self, seed, initial_policy_path):
        return D2DSPLActorCriticTracesAgent(self.num_actions, self.discretizer, self.max_num_samples_for_classifier, self.normalizer, self.milestone_episodes, 
                           self.hidden_layer_sizes, seed)