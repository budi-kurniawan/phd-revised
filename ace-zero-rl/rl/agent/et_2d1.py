__author__ = 'bkurniawan'import mathfrom .. import rl_utilsfrom rl.agent.eligibility_traces import EligibilityTracesAgent
class EligibilityTraces2D1Agent(EligibilityTracesAgent):    ### An agent implementing eligibility traces and Q-learning    def __init__(self, params_filename=None):        super(EligibilityTraces2D1Agent, self).__init__()
    actions = ['no_command', 'set_heading(10)', 'set_heading(-10)']        def calculate_t(self, reward):        self.t += reward * EligibilityTracesAgent.GAMMA * EligibilityTracesAgent.LAMBDA    def is_terminal(self, state):        return False    def is_in_goal(self, state):        R, ata, aa, dv = rl_utils.get_R_ata_aa_from_state(state)        #return R >= 9 and R <= 46 and math.fabs(aa) <= 60 and math.fabs(ata) <= 30        return math.fabs(ata) <= 40    def get_state(self, entity_state, threat_state):        # goldilock is 9 <= i <= 46        # common_attributes = ['x','y','z','psi','psi_c','theta','theta_c','phi','v','v_c']        # use psi to get heading degree, psi_c to pass t        # SetHeadingGLoadCmd(psi_c=threat_bearing, gload_c=5)        R, ata, aa = rl_utils.get_R_ata_aa_from_entities(entity_state, threat_state)        if R > 131:            R = 131        return str(R) + "|" + str(ata) + "|" + str(aa)#     def get_reward(self, state):#         return 1 if self.consecutive_in_goal >= rl_utils.MIN_NUM_IN_GOAL and self.is_in_goal(state) else 0    def get_reward(self, state):        if self.is_in_goal(state):            return 1 if self.consecutive_in_goal >= rl_utils.MIN_NUM_IN_GOAL else 0.1        else:            return 0    def log(self, t, reward, prev_state_action, q, e):        if t > 10:            return        log_file = rl_utils.context.log_file        blue = self.beliefs.entity_state        red = self.beliefs.threat_state        R, ata, aa = rl_utils.get_R_ata_aa_from_entities(blue, red)        log_file.write(str.format("t:{0}, blue({1},{2}), red({3},{4}), r:{5}, blue.psi:{6} red.psi:{7}\n",                                   t, blue.x, blue.y, red.x, red.y, R, blue.psi, red.psi))        log_file.write(str.format("ATA:{0}, AA:{1}, prev_sa:{2}, reward:{3}\n", ata, aa, prev_state_action, reward))        #log_file.write(str.format("contact range:{0}, contact ata:{1}, contact aa:{2}\n", blue.contact_range, blue.contact_ata, blue.contact_aa))        log_file.write("v:" + str(blue.v) + "/" + str(red.v) + "\n")        log_file.write("q:" + str(q) + "\n")        log_file.write("e:" + str(e) + "\n\n")        