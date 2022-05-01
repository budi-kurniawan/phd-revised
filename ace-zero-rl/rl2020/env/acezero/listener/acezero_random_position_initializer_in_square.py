from rl2020.env.acezero.listener.acezero_simple_random_position_initializer import AceZeroSimpleRandomPositionInitializer
from rl2020.util.util import override

class AceZeroRandomPositionInitializerInSquare(AceZeroSimpleRandomPositionInitializer):
    """ Positions Red within a square of 1600"""
    @override(AceZeroSimpleRandomPositionInitializer)
    def get_red_initials(self, init):
        square_length = 1600
        x = (self.random.random() - 0.5) * 2 * square_length
        y = (self.random.random() - 0.5) * 2 * square_length
        z = 0
        psi = (self.random.random() - 0.5) * 2 * 180
        return (x, y, z, psi)