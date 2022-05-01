import rl
import rl_utils
import mysql.connector
import time

# must have installed mysql connector: pip install mysql-connector-python
# clone table:
# CREATE TABLE newtable LIKE oldtable; 
# INSERT newtable SELECT * FROM oldtable;
if __name__ == '__main__':
    start_time = time.time()
    print("Start ", start_time)
    num_actions = 5
    num_agents = 2

    create_table_sql = """CREATE TABLE q
        (state CHAR(20), action SMALLINT UNSIGNED, agent_id SMALLINT, counter INT UNSIGNED, value DOUBLE,
        INDEX state_action_idx (state, action)) """
    
    print(create_table_sql)
    cnx = mysql.connector.connect(user=rl_utils.dbuser, password=rl_utils.dbpassword,
        host=rl_utils.dbhost, database=rl_utils.dbname)
    cursor = cnx.cursor()
#     cursor.execute(create_table_sql)
#     cnx.commit()
    
    # This will create 3,614,160 * 21 = 75,897,360 records
    for R in range(0, 132):
        print(R)
        for ata in range(-180, 190, 10):
            for aa in range(-180, 190, 10):
                for dv in range(-100, 110, 10):
                    state = str(R) + '|' + str(ata) + '|' + str(aa) + '|' + str(dv)
                    for action in range(num_actions):
                        for agent in range(1, num_agents + 1):
                            sql = "INSERT INTO q (state, action, agent_id, counter, value) VALUES (%s, %s, %s, 0, 0)"
                            val = (state, action, agent)
                            cursor.execute(sql, val)
                    cnx.commit()
    cursor.close()
    cnx.close()
    end_time = time.time()
    print("Total time:", end_time - start_time)

#     cnx.close()