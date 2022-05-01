from ace_zero_core.agents.fsm_agent.state_agent import StateAgent
from ace_zero_core.pilot_commands import SetHeadingGLoadCmd
import ace_zero_core.utils as ut

from rl2020.util.util import override

class RestrictedPurePursuitAgent(StateAgent):
    """

    def set_heading(self, delta):
        my_heading = self.beliefs.entity_state.heading
        new_heading = my_heading + delta
        self.commands.append(SetHeadingGLoadCmd(psi_c=new_heading, gload_c=5))


    def speed_pct(self, delta): #increase/decrease speed by delta%
        max_speed = self.beliefs.entity_state.v_max
        current_speed = self.beliefs.entity_state.v
        new_speed = (1 + delta/100.0) * current_speed
        self.commands.append(SetSpeedCmd(v_c=min(new_speed, max_speed)))


    Single-state agent that pursues a target by pointing the aircraft nose
    directly at it.

    During execution the relative bearing to the threat is calculated and a
    command is issued to turn the aircraft to fly toward it.
    
    Similar to PurePursuitAgent, but restricted_pure_pursuit_agent in what it can do
    """
    override(StateAgent)
    def execute(self, t, dt):
        StateAgent.execute(self, t, dt)
 
        if self.beliefs.threat_state:
            # Determine the bearing to the threat aircraft
            entity = self.beliefs.entity_state
            threat = self.beliefs.threat_state
            threat_bearing = ut.relative_bearing(entity.x, entity.y,
                                                 threat.x, threat.y)
 
            # Issue the change heading command
            if not ut.is_close(threat_bearing, entity.desired_heading):                
                entity_heading = entity.heading
                # restrict heading change to 10 degrees
                if threat_bearing > entity_heading + 10:
                    threat_bearing = entity_heading + 10
                elif threat_bearing < entity_heading - 10:
                    threat_bearing = entity_heading - 10
                self.commands.append(SetHeadingGLoadCmd(psi_c=threat_bearing, gload_c=5))