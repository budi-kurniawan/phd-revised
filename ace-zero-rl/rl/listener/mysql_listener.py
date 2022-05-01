from rl.listener.learning_listener import LearningListener
import mysql.connector
import rl
from rl import rl_utils

class MySQLListener(LearningListener):
    def __init__(self, context):
        super(MySQLListener, self).__init__(context)
        
    def trial_start(self):
        connection = mysql.connector.connect(user=rl_utils.dbuser, password=rl_utils.dbpassword,
            host=rl_utils.dbhost, database=rl_utils.dbname)
        cursor = connection.cursor()
        context = self.context
        context.connection = connection
        context.cursor = cursor
        
    def trial_end(self):
        context = self.context
        context.cursor.close()
        context.connection.close()