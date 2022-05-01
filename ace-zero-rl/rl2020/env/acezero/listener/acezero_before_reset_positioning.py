import math
from rl2020.listener.step_listener import StepListener
from rl2020.util.util import override
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.listener.impl.seedable_trial_listener import SeedableTrialListener
from rl2020.listener.trial_listener import TrialListener
from ace_zero_core.utils import constrain_180
from rl2020.env.acezero.ace_zero_util import get_144_initial_position_tuples
from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl import rl_util, rl_utils

class AceZeroBeforeResetPositioning(AceZeroBasicTestA):
    """ Do before env.reset() positioning which is more precise especially for Rl vs RL"""
    @override(EpisodeListener)
    def before_episode(self, event):
#         sim = event.env.ace0.sim
#         viper = sim.viper
#         cobra = sim.cobra
#         viper_state = viper.get_state()
#         cobra_state = cobra.get_state()
        blue, red, _ = self.positions[event.activity_context.episode - 1]
        
        rl_utils.blue_default_initial['x'] = blue[0]
        rl_utils.blue_default_initial['y'] = blue[1]
        rl_utils.blue_default_initial['psi'] = blue[2]
        rl_utils.red_default_initial['x'] = red[0]
        rl_utils.red_default_initial['y'] = red[1]
        rl_utils.red_default_initial['psi'] = red[2]
#         viper.set_position(blue[0], blue[1], 0)
#         viper.set_orientation(blue[2], viper_state.theta, viper_state.phi)
#         cobra.set_position(red[0], red[1], 0)
#         cobra.set_orientation(red[2], cobra_state.theta, cobra_state.phi)

    @override(EpisodeListener)
    def after_episode(self, event):
        ep = event.activity_context.episode
        blue, red, behaviour = self.positions[ep - 1]
        self.values_by_behaviour.get(behaviour).append(event.avg_reward)
        if ep == len(self.positions):
            event.stopper.active = True