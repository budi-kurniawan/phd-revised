import rl
import rl_utils
import mysql.connector
import time

# must have installed mysql connector: pip install mysql-connector-python
# clone table:
# CREATE TABLE newtable LIKE oldtable; 
# INSERT newtable SELECT * FROM oldtable;
#
# for remote access (Windows): GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'IP' IDENTIFIED BY 'PASSWORD';
# FLUSH PRIVILEGES; 

# for remote access (Linux) see https://devdocs.magento.com/guides/v2.0/install-gde/prereq/mysql_remote.html
if __name__ == '__main__':
    start_time = time.time()
    print("Start")
    connection = mysql.connector.connect(user=rl_utils.dbuser, password=rl_utils.dbpassword,
        host=rl_utils.dbhost, database=rl_utils.dbname)
    cursor = connection.cursor()
    state = '0|0|0'
    action = 0
    agent_id = 1
    value = 1.234
    
#     for i in range(1000):
#         rl_utils.update_q_value_in_db(connection, cursor, state, action, agent_id, value)
#         result = rl_utils.get_q_value_from_db(cursor, state, action)    
#         print(i)
#     for x in result:
#         print(x)

    selected = rl_utils.get_q_value_from_db(cursor, state, action)
    print("selected:", selected)
    
    cursor.close()    
    connection.close()
    end_time = time.time()
    print("Total time:", end_time - start_time)

#     connection.close()