""" An MFECAssistant provides helper methods whose implementations are specific to a problem """
class MFECAssistant:
    # project state, normally to reduce dimensionality
    def project(self, state):
        return state
    
    # Returns True if a and b are close enough
    def near(self, a, b):
        return False
