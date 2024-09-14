import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username  TEXT NOT NULL,
        email  TEXT NOT NULL,
        age  INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Product")
    data = cursor.fetchall()
    return data

def add_user(username, email, age):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age,balance) VALUES (?,?,?,?)",
                   (f"{username}", f"{email}", f"{age}", "1000"))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM Users")
    users = cursor.fetchall()
    users = {user[0] for user in users}
    if username in users:
        return True
    else:
        return False

