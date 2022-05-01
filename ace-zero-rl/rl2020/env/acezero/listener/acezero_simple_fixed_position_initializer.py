import math
from rl2020.listener.step_listener import StepListener
from rl2020.util.util import override
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.listener.impl.seedable_trial_listener import SeedableTrialListener
#from rl.rl_utils import red_default_initial

class AceZeroSimpleFixedPositionInitializer(SeedableTrialListener, StepListener, EpisodeListener):
    def __init__(self):
        pass

    """ Positions Red at the beginning of each episode (Blue will always be at (0, 0, 0, 0))."""
    @override(EpisodeListener)
    def before_episode(self, event):
        sim = event.env.sim
        cobra = sim.cobra        
        # x should move from 1500 to 0 in 10 steps, y from -300 to 300 in 10 steps, z and psi remain 0 all the time
        cobra_state = cobra.get_state()
        init  = (cobra_state.x, cobra_state.y, cobra_state.z, cobra_state.psi)
        red_initials = self.__get_red_initials(event.activity_context.episode, init)
        cobra.set_position(red_initials[0], red_initials[1], red_initials[2])
        cobra.set_orientation(red_initials[3], cobra_state.theta, cobra_state.phi)

    def __get_red_initials(self, episode, init):
        r = 1500
        blue_location_angle = (episode - 1) * 3.6
        rads = math.radians(blue_location_angle)
        x = r * math.cos(rads)
        y = r * math.sin(rads)
        z = 0
        psi = 0
        return (x, y, z, psi)
