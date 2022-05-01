from datetime import datetime
from rl2020.util.util import override
from rl2020.listener.session_listener import SessionListener

class SessionLogger(SessionListener):
    def __init__(self, description):
        self.description = description
        self.filename = 'description.txt'

    @override(SessionListener)
    def before_session(self, event):
        out_path = event.activity_context.out_path
        file = open(out_path + '/' + self.filename, 'w')
        file.write(self.description + '\n')
        file.write('Learning started at ' + str(datetime.now()) + '\n')
        file.close()
        
    @override(SessionListener)
    def after_session(self, event):
        out_path = event.activity_context.out_path
        file = open(out_path + '/' + self.filename, 'a+')
        file.write('Learning finished at ' + str(datetime.now()) + '\n')
        file.close()        