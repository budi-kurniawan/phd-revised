import numpy as np
from rl2020.agent.mfec.mfec_assistant import MFECAssistant

class AceZeroMFECAssistant(MFECAssistant):
    def __init__(self):
        self.rs = np.random.RandomState(0)
        self.projection = self.rs.randn(
            4,4
        ).astype(np.float32)

    def project(self, state):
        s = np.array(((state[0] / 4500.0) - 1, state[1] / 180.0, state[2] / 180.0, state[3] / 40.0))
        #s = np.array([(state[0] / 4500.0) - 1], [state[1] / 180.0], [state[2] / 180.0], [state[3] / 40.0])
        #s = np.dot(self.projection, s.flatten())
        #print('shape:', s.shape)
        #print('projected state:' , type(s), s)
        return s
    
    def near(self, a, b):
        return False