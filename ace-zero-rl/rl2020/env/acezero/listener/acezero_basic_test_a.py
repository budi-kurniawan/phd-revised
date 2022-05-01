from rl2020.listener.step_listener import StepListener
from rl2020.util.util import override
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.listener.impl.seedable_trial_listener import SeedableTrialListener
from rl2020.listener.trial_listener import TrialListener
from ace_zero_core.utils import constrain_180
from rl2020.env.acezero.ace_zero_util import get_144_initial_position_tuples

class AceZeroBasicTestA(SeedableTrialListener, StepListener, EpisodeListener):
    """ Generates blue and red initial positions and store them in self.positions.
        Blue is always in (0, 0) and Red in (1500,0). Red rotates by 30 degrees and for every 12 rotations of red, blue is rotated by 30 degrees.
        This will create 144 different position positions."""
    @override(TrialListener)
    def before_trial(self, event):
        super().before_trial(event)
        # we just need one blue_location_angle (0 degree) because other values of it would create duplicates
        r = 1500
        self.positions = get_144_initial_position_tuples(r)
        self.values_by_behaviour = {'d':[], 'h':[], 'n':[], 'o':[]}

    @override(TrialListener)
    def after_trial(self, event):
        activity_context = event.activity_context
        out_path = activity_context.out_path
        trial = activity_context.trial
        self.values_file = open(out_path + '/values-by-behaviour-' + str(trial).zfill(2) + '.txt', 'w')
        d = self.values_by_behaviour.get('d')
        h = self.values_by_behaviour.get('h')
        n = self.values_by_behaviour.get('n')
        o = self.values_by_behaviour.get('o')
        self.values_file.write('defensive,' + str(sum(d)/len(d)) + '\n')
        self.values_file.write('head-on,' + str(sum(h)/len(h)) + '\n')
        self.values_file.write('neutral,' + str(sum(n)/len(n)) + '\n')
        self.values_file.write('offensive,' + str(sum(o)/len(o)) + '\n')
        self.values_file.close()
    
    @override(EpisodeListener)
    def after_env_reset(self, event):
        sim = event.env.sim
        viper = sim.viper
        cobra = sim.cobra
        viper_state = viper.get_state()
        cobra_state = cobra.get_state()
        blue, red, _ = self.positions[event.activity_context.episode - 1]
        viper.set_position(blue[0], blue[1], 0)
        viper.set_orientation(blue[2], viper_state.theta, viper_state.phi)
        cobra.set_position(red[0], red[1], 0)
        cobra.set_orientation(red[2], cobra_state.theta, cobra_state.phi)

    @override(EpisodeListener)
    def after_episode(self, event):
        ep = event.activity_context.episode
        blue, red, behaviour = self.positions[ep - 1]
        self.values_by_behaviour.get(behaviour).append(event.avg_reward)
        if ep == len(self.positions):
            event.stopper.active = True