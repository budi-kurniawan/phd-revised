import matplotlib.pyplot as plt
import numpy as np
from rl2020.listener.trial_listener import TrialListener
from rl2020.listener.episode_listener import EpisodeListener
from rl2020.util.util import override

class AceZeroTrajectoryManager(TrialListener, EpisodeListener):
    def __init__(self):
        self.trajectories_file = None
        self.writer = None

    @override(EpisodeListener)
    def after_episode(self, event):
        activity_context = event.activity_context
        trial = activity_context.trial
        episode = activity_context.episode
        out_path = activity_context.out_path
        sim = event.env.sim
        viper_trace = sim.viper.fcs.platform.trace
        cobra_trace = sim.cobra.fcs.platform.trace
        if self.trajectories_file is not None:
            viper_trace_2d = [x[:3] for x in viper_trace] #grab dt, x, y
            cobra_trace_2d = [x[:3] for x in cobra_trace]
            self.trajectories_file.write(str(episode) + ",viper," + str(viper_trace_2d) + '\n')
            self.trajectories_file.write(str(episode) + ",cobra," + str(cobra_trace_2d) + '\n')
        chart_path = out_path + '/trajectory-' + str(trial).zfill(2) + '-' + str(episode).zfill(8) + '.png'
        self.__draw_2d_trajectories(episode, viper_trace, cobra_trace, chart_path)
                
    @override(TrialListener)
    def before_trial(self, event):
        activity_context = event.activity_context
        trial = activity_context.trial
        out_path = activity_context.out_path
        self.trajectories_file = open(out_path + '/trajectories-' + str(trial).zfill(2) + '.txt', 'w')

    @override(TrialListener)
    def after_trial(self, event):
        ac = event.activity_context
        trial = ac.trial
        out_path = ac.out_path
        self.trajectories_file.close()
        duration_in_seconds = (ac.trial_end_time - ac.trial_start_time).total_seconds()
        times_file = open(out_path + '/times.txt', 'a+')
        msg = 'Trial ' + str(trial) + ' finished in ' + str(duration_in_seconds) + ' seconds.'
        times_file.write(msg + '\n')
        times_file.close()

    def __draw_2d_trajectories(self, id, viper_trace, cobra_trace, path, waypoints=None, waypoint_size=100.0):
        viper_x = [x[1] for x in viper_trace]
        viper_y = [x[2] for x in viper_trace]
        cobra_x = [x[1] for x in cobra_trace]
        cobra_y = [x[2] for x in cobra_trace]
    
        xmin = min(min(viper_x), min(cobra_x))
        xmax = max(max(viper_x), max(cobra_x))
        ymin = min(min(viper_y), min(cobra_y))
        ymax = max(max(viper_y), max(cobra_y))
        min_ = 1.1 * min(xmin, ymin)
        max_ = 1.1 * max(xmax, ymax)
    
        arrow_width = xmax - xmin
        height = ymax - ymin
        fig_width, fig_height = 10, 10
#         if arrow_width < height:
#             fig_width *= arrow_width / height
#         else:
#             fig_height *= height / arrow_width
            
        fig = plt.figure(figsize=(fig_width, fig_height))
        p = plt.title('Test ' + str(id), loc='center')
        plt.rcParams["legend.loc"] = 'upper left'
        plt.xlim([min_, max_])
        plt.ylim([min_, max_])
    
        p = plt.grid(b=True, which='major', linewidth=0.6, color='grey', linestyle='-')
        p = plt.grid(b=True, which='minor', linewidth=0.2, color='lightgrey', linestyle='-')
        plt.minorticks_on()
        #p = plt.axes().set_aspect('equal')
        plt.plot(viper_x, viper_y, c='blue', alpha=0.5, lw=2, markevery=100, marker='.', linestyle='-')
        plt.plot(cobra_x, cobra_y, c='red', alpha=0.5, lw=2, markevery=100, marker='.', linestyle='-')
    
            # Waypoints
        if waypoints:
            for wp in waypoints:
                x, y = wp
                c = mpatches.Circle((x, y), waypoint_size, fill=False, ec='grey')
                plt.axes().add_patch(c)
                #arrow = Arrow(x, y, 1000, 1000, 10.0, ec='black')
                #plt.arrow(x, y, 1000, 1000, 100.0, ec='blue')
    
        # Viper Arrows
        ''' Problem with plt.arrow() is it needs to have a head_length, 
            which is not suitable in the case we want the arrow head point to be on the last trace point
        '''
        r = 1000
        x, y, psi = viper_trace[-1][1], viper_trace[-1][2], viper_trace[-1][4]
        self.__draw_arrow(plt, r, x, y, psi, 'blue')
        x, y, psi = cobra_trace[-1][1], cobra_trace[-1][2], cobra_trace[-1][4]
        self.__draw_arrow(plt, r, x, y, psi, 'red')
        
        p = plt.text(viper_x[-1] + 50, viper_y[-1] + 50, 'Viper', color='blue')    
        p = plt.text(cobra_x[-1] + 50, cobra_y[-1] + 50, 'Cobra', color='red')
        blue_legend = '({:.2f}, {:.2f}, {:.2f}\N{DEGREE SIGN})'.format(viper_trace[0][1], viper_trace[0][2], viper_trace[0][4]) \
                + ' \u2192 ({:.2f}, {:.2f}, {:.2f}\N{DEGREE SIGN})'.format(viper_trace[-1][1], viper_trace[-1][2], viper_trace[-1][4])
        red_legend = '({:.2f}, {:.2f}, {:.2f}\N{DEGREE SIGN})'.format(cobra_trace[0][1], cobra_trace[0][2], cobra_trace[0][4]) \
                + ' \u2192 ({:.2f}, {:.2f}, {:.2f}\N{DEGREE SIGN})'.format(cobra_trace[-1][1], cobra_trace[-1][2], cobra_trace[-1][4])
        plt.legend((blue_legend, red_legend))
        plt.savefig(path)
        plt.close()

    def __draw_3d_trajectories(self, trace1, trace2, path):
        """ Draw the aircraft trajectories in 3D. """
        title = 'Two Aircraft Trajectory Plot'
        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca(projection='3d')
        plt.grid(True)
        plt.title(title, loc='left')
        plt.axis('equal')
    
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
    
        ta1, xa1, ya1, za1 = ([], [], [], [])
        for timeslice in trace1:
            t, x, y, z, psi, theta, phi, v, weight, fuel = timeslice
            ta1.append(t)
            xa1.append(x)
            ya1.append(y)
            za1.append(z)
    
        xmin = min(xa1)
        xmax = max(xa1)
        ymin = min(ya1)
        ymax = max(ya1)
        zmin = min(za1)
        zmax = max(za1)
    
        ta2, xa2, ya2, za2 = ([], [], [], [])
        for timeslice in trace2:
            t, x, y, z, psi, theta, phi, v, weight, fuel = timeslice
            ta2.append(t)
            xa2.append(x)
            ya2.append(y)
            za2.append(z)
    
        xmin = min(min(xa2), xmin)
        xmax = max(max(xa2), xmax)
        ymin = min(min(ya2), ymin)
        ymax = max(max(ya2), ymax)
        zmin = min(min(za2), zmin)
        zmax = max(max(za2), zmax)
    
        # Fix aspect ratio
        max_range = np.array([xmax - xmin, ymax - ymin, zmax - zmin]).max() / 2.0
        mid_x = (xmax + xmin) * 0.5
        mid_y = (ymax + ymin) * 0.5
        mid_z = (zmax + zmin) * 0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
        # Plot Trajectories
        plt.plot(xa1, ya1, za1, color='C0')
        plt.plot(xa2, ya2, za2, color='C3')
    
        # Draw t=0.0 marker for trace1
        #ax.text(xa1[0], ya1[0], za1[0]+1, "t = %2.1f" % ta1[0], color='b', alpha=0.5)
        #ax.scatter(xa1[0], ya1[0], za1[0], color='b', marker='o', s=100, alpha=0.5)
        # and now trace2
        #ax.text(xa2[0], ya2[0], za2[0]+1, "t = %2.1f" % ta2[0], color='r', alpha=0.5)
        #ax.scatter(xa2[0], ya2[0], za2[0], color='r', marker='o', s=100, alpha=0.5)
    
        # Draw t=tmax marker for trace1
        ax.text(xa1[-1]+50, ya1[-1]+50, za1[-1]+750, "t = %2.1f s" % ta1[-1], color='C0', alpha=0.9)
        ax.scatter(xa1[-1], ya1[-1], za1[-1], color='C0', marker='>', s=100, alpha=0.5)
        # and now for trace 2
        ax.text(xa2[-1]+50, ya2[-1]+50, za2[-1]+750, "t = %2.1f s" % ta2[-1], color='C3', alpha=0.9)
        ax.scatter(xa2[-1], ya2[-1], za2[-1], color='C3', marker='>', s=100, alpha=0.5)
        plt.savefig(path)
        plt.close()
     
    def __draw_arrow(self, plt, r, x0, y0, psi, color):
        import math
        theta = math.radians(psi - 30)
        x1 = x0 - r * math.cos(theta)
        y1 = y0 - r * math.sin(theta)
        theta = math.radians(psi + 30)
        x2 = x0 - r * math.cos(theta)
        y2 = y0 - r * math.sin(theta)
        x1, y1 = [x1, x0], [y1, y0]
        x2, y2 = [x2, x0], [y2, y0]
        plt.plot(x1, y1, x2, y2, color=color)