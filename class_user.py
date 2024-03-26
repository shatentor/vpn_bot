from data_base.mariadb_conn import connect_to_database
from pass_for_user import generate_password
import mariadb


def execute_query(query, parameters=None):
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        if parameters:
            cur.execute(query, parameters)
        else:
            cur.execute(query)
        try:
            result = cur.fetchall()
            return result
        #in case, when cursor is empty
        except mariadb.Error:
            pass
    except mariadb.Error:
        print ('Error: {e}')
        #create new connection
        conn = connect_to_database()
        cur = conn.cursor()
        if parameters:
            cur.execute(query, parameters)
        else:
            cur.execute(query)
        try:
            result = cur.fetchall()
            return result
        except mariadb.Error:
            pass


class User:
    def __init__(self, username):
        self.username = str(username)

    def get_chat_id(self):
        result = execute_query("SELECT chat_id FROM users WHERE username = ?", (self.username,))
        return result[0][0] if result else None

    def get_path_to_config(self, number):
        result = execute_query(f'SELECT config_path_{number} FROM users WHERE username = ?', (self.username,))
        return result[0][0] if result else None

    def get_user_password(self):
        result = execute_query("SELECT current_pass FROM users WHERE username = ?", (self.username,))
        return str(result[0][0]) if result else None

    def get_number_of_configs(self):
        result = execute_query("SELECT number_of_configs FROM users WHERE username = ?", (self.username,))
        return result[0][0] if result else None

    def plus_config_number(self):
        execute_query("UPDATE users SET number_of_configs = number_of_configs + 1 WHERE username = ?", (self.username,))
        return None

    def create_new_password(self):
        execute_query("UPDATE users SET current_pass = ? WHERE username = ?", (generate_password(), self.username))
        return None

    def is_user(self):
        result = execute_query('SELECT EXISTS(SELECT username FROM users WHERE username = ?)', (self.username,))
        return result[0][0] == 1 if result else False


    def create_new_user(self, password, chat_id):
        execute_query("INSERT INTO users (username, current_pass, chat_id) VALUES(?, ?, ?)", (self.username, password, chat_id))
        execute_query("INSERT INTO configs_dates (username, chat_id) VALUES (?, ?)", (self.username, chat_id))
        return None

    def set_date_config(self, number):
        execute_query(f"UPDATE configs_dates SET config_{number} = NOW() WHERE username = ?", (self.username,))
        return None

