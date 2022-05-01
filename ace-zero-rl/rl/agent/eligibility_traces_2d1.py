__author__ = 'bkurniawan'
from rl.agent.eligibility_traces7 import EligibilityTracesAgent7
from rl import rl_utils
# 2D agent using Q-learningclass EligibilityTraces2D1Agent(EligibilityTracesAgent7):    ### A modified coarse Q-learning agent
    def __init__(self, params_filename=None):        super(EligibilityTraces2D1Agent, self).__init__()
    actions = ['no_command', 'change_speed_by_percentage(-10)', 'change_speed_by_percentage(10)',                'set_heading(10)', 'set_heading(-10)']
    def calculate_t(self, reward):        self.t += reward * EligibilityTracesAgent.GAMMA * EligibilityTracesAgent.LAMBDA
    def is_terminal(self, state):        return False
    def is_in_goal(self, state):        R, ata, aa = rl_utils.get_R_ata_aa_from_state(state)        return R >= 9 and R <= 46 and aa <= 60 and ata <= 30
    def get_state(self, entity_state, threat_state):        # goldilock is 9 <= i <= 46        # common_attributes = ['x','y','z','psi','psi_c','theta','theta_c','phi','v','v_c']        # use psi to get heading degree, psi_c to pass t        # SetHeadingGLoadCmd(psi_c=threat_bearing, gload_c=5)        R, ata, aa = rl_utils.get_R_ata_aa_from_entities(entity_state, threat_state)        if R > 131:            R = 131        return str(R) + "|" + str(ata) + "|" + str(aa)
    def get_reward(self, state):        return 1 if self.consecutive_in_goal >= rl_utils.MIN_NUM_IN_GOAL and self.is_in_goal(state) else 0

    def log(self, t, reward, prev_state_action, q, e):        # The log file is in q_snapshots/        if t > 5:            return        entity_state = self.beliefs.entity_state        threat_state = self.beliefs.threat_state        R, ata, aa = rl_utils.get_R_ata_aa_from_entities(entity_state, threat_state)        self.log_file.write(str.format("t:{0}, reward:{1}, prev sa:{2}\n", t, reward, prev_state_action))        self.log_file.write(str.format("R:{0}, blue.psi:{1}, red.psi:{2}, ata: {3}, aa:{4}\n", R, entity_state.psi, threat_state.psi, ata, aa))        self.log_file.write("q:" + str(q) + "\n")        self.log_file.write("e:" + str(e) + "\n\n")