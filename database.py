import sqlite3

global connection

def wipe_database():
    global connection
    if connection is None:
        print("connection is None")
        return
    
    try:
        c = connection.cursor()
        c.execute("DROP TABLE accounts")
    except Exception as e:
        print(e)
    finally:
        c.close()

def create_connection(path):
    global connection
    try:
        connection = sqlite3.connect(f"{path}.sqlite")
    except Exception as e:
        print(e)
    finally:
        return connection

def create_table():
    global connection
    if connection is None:
        print("connection is None")
        raise Exception
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE account(" + 
            "id INTEGER," +
            "summoner_username VARCHAR," +
            "region  VARCHAR," +
            "username  VARCHAR," +
            "password BLOB" +
        ");")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        
def save_to_table(table_name, column_names, values):
    global connection
    if connection is None:
        print("connection is None")
        return
    

    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM {table_name} WHERE {column_names[0]} = {values[0]} ''')
    if len(cursor.fetchall()) >= 1:
        cursor.execute(f'''UPDATE {table_name} SET {column_names} = (?, ?, ?, ?, ?) WHERE {column_names[0]} = {values[0]}''', (values[0], values[1], values[2], values[3], values[4]))
        cursor.execute(f'''SELECT * FROM {table_name} WHERE {column_names[0]} = ? ''', (values[0],))
    else:
        cursor.execute(f"INSERT INTO {table_name} {column_names} VALUES (?, ?, ?, ?, ?) ", (values[0], values[1], values[2], values[3], values[4]))
    
    cursor.close()
    connection.commit()
    
        
def load_from_table(table_name, column_name, value):
    if connection is None:
        print("connection is None")
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = {value}")
        return cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def load_all_from_table(table_name):
    if connection is None:
        print("connection is None")
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def delete_from_table(table_name, column_name, value):
    if connection is None:
        print("connection is None")
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = {value}")
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def count_from_table(table_name, column_name):
    if connection is None:
        print("connection is None")
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT({column_name}) FROM {table_name}")
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def delete_all_from_table(table_name):
    if connection is None:
        print("connection is None")
        return
    
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name}")
    connection.commit()
    cursor.close()
    


