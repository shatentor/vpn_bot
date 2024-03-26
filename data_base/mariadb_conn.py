import mariadb

def connect_to_database():
    try:
        conn = mariadb.connect(
            user="user",
            password="*******",
            host="**********",
            port=3306,
            database="vpn_bot",
            autocommit=True
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
