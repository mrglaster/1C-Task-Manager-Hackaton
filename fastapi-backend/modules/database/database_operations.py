import base64
import sqlite3 as sl
import random
import string


def create_connection(db_file: str):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    return sl.connect(db_file)


def is_valid_user(connection, login, password):
    if not login or not password:
        return False
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    user = cursor.fetchone()
    return user is not None


def generate_token():
    symbols = string.ascii_letters + string.digits
    return ''.join(random.choice(symbols) for _ in range(254))


def process_registration(connection, login, password):
    if is_valid_user(connection, login, password):
        return {"status": 221, "description": "There is already a user with such name!"}
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
    token = generate_token()
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO sessions (user_id, token) VALUES (?, ?)", (user_id, token))
    cursor.execute("INSERT INTO data(user_id, data) VALUES(?, ?)", (user_id, ""))
    connection.commit()
    return {"status": 200, "token": token, "description": "You have been successfully registered"}


def process_authorisation(connection, login, password):
    if is_valid_user(connection, login, password):
        cursor = connection.cursor()
        query = "SELECT id FROM users WHERE login=? AND password=?"
        cursor.execute(query, (login, password))
        user_id = cursor.fetchone()[0]
        token = generate_token()
        update_query = "UPDATE sessions SET token = ? WHERE user_id = ?"
        cursor.execute(update_query, (token, user_id))
        connection.commit()
        return {"status": 200, "token": token, "description": "You have been authorized!"}
    return {"status": 403, "description": "Access denied!"}


def is_valid_token(connection, token):
    if not token:
        return False
    cursor = connection.cursor()
    user = "SELECT id FROM sessions WHERE token=?;"
    cursor.execute(user, [token])
    user_id = cursor.fetchone()
    return user_id is not None


def get_userid_by_token(cursor, token):
    user_id_query = "SELECT id FROM sessions WHERE token=?"
    cursor.execute(user_id_query, [token])
    return cursor.fetchone()


def get_data(connection, token):
    if is_valid_token(connection, token):
        cursor = connection.cursor()
        user_id = get_userid_by_token(cursor, token)
        data_query = "SELECT data from data WHERE user_id=?"
        cursor.execute(data_query, user_id)
        data = cursor.fetchone()
        return {"status": 200, "data": data, "description": "Here's your data"}
    return {"status": 403, "description": "Access denied!"}


def upload_data(connection, token, data):
    if data is None:
        return {"status": 400, "description": "bad request"}
    if is_valid_token(connection, token):
        cursor = connection.cursor()
        user_id = get_userid_by_token(cursor, token)
        update_query = "UPDATE data SET data = ? WHERE user_id = ?"
        cursor.execute(update_query, (data, user_id[0]))
        connection.commit()
        return {"status": 200, "description": "The data has been updated!"}
    return {"status": 403, "description": "Access denied!"}
