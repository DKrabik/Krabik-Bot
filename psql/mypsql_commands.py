import psycopg2
from psycopg2 import Error

def create_connection(host_name, user_name, user_password, db_name = None):
    connection = None
    try:
        connection = psycopg2.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print(f"Connection to '{host_name}:{db_name}' successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def query(connection, query, get = False):
    cursor = connection.cursor()
    temp = False
    try:
        cursor.execute(query)
        if (get):
            temp = cursor.fetchall()
        print(f"{query} - Query successful")
    except Error as e:
        print(f"{query} - The error '{e}' occurred")
    finally:
        return temp

        

def select_from_settings(connection, select, server_id):
    return query(connection, f'SELECT {select} FROM settings WHERE server_id = {server_id};', get=True)[0][0]
    
def change_settings(connection, update, param, server_id):
    return query(connection, f'UPDATE settings SET {update} = {param} WHERE server_id = {server_id}')

