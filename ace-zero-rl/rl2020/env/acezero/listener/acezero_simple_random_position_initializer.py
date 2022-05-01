from rl2020.listener.step_listener import StepListener
from rl2020.util.util import override
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.listener.impl.seedable_trial_listener import SeedableTrialListener
#from rl.rl_utils import red_default_initial

class AceZeroSimpleRandomPositionInitializer(SeedableTrialListener, StepListener, EpisodeListener):
    """ Positions Red at the beginning of each episode (Blue will always be at (0, 0, 0))."""
    @override(EpisodeListener)
    def after_env_reset(self, event):
        sim = event.env.sim
        cobra = sim.cobra
        cobra_state = cobra.get_state()
        init  = (cobra_state.x, cobra_state.y, cobra_state.z, cobra_state.psi)
        red_initials = self.get_red_initials(init)
        cobra.set_position(red_initials[0], red_initials[1], red_initials[2])
        cobra.set_orientation(red_initials[3], cobra_state.theta, cobra_state.phi)

    def get_red_initials(self, init): # do not make this private __get_red_initials() so it can be overriden
        r = self.random.random() - 0.5 # return -0.5..0.5
        x = init[0] + r * 10
        y = init[1] + r * 2
        z = 0
        psi = init[3] + r * 2
        return (x, y, z, psi)