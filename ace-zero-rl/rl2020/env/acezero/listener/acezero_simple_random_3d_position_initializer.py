from rl2020.util.util import override
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
#from rl.rl_utils import red_default_initial

class AceZeroSimpleRandom3DPositionInitializer(AceZeroSimpleRandomPositionInitializer):
    """ Positions Red at the beginning of each episode (Blue will always be at (0, 0, 10_000, 0))."""
    def get_red_initials(self, init): # do not make this private __get_red_initials() so it can be overriden
        r = self.random.random() - 0.5 # return -0.5..0.5
        x = init[0] + r * 10
        y = init[1] + r * 2
        z = init[2] + r * 10
        psi = init[3] + r * 2
        return (x, y, z, psi)