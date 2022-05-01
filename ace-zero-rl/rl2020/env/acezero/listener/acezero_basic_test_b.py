from rl2020.env.acezero.listener.acezero_basic_test_a import AceZeroBasicTestA
from rl2020.util.util import override

class AceZeroBasicTestB(AceZeroBasicTestA):
    @override(AceZeroBasicTestA)
    def after_env_reset(self, event):
        super().before_episode(event)
        sim = event.env.sim
        viper = sim.viper
        viper.set_speed(1.1 * viper.get_state().v_c)