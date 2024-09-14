import sqlite3

connection = sqlite3.connect('not_telegram1.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance TEXT NOT NULL
)
''')

# for i in range(10):
#     i += 1
#     cursor.execute("INSERT INTO Users (username, email, age,balance) VALUES (?,?,?,?)", (f"User{i}",f"example{i}@gmail.com",f"{i*10}","1000"))
cursor.execute("UPDATE Users SET balance = ? WHERE id%2 != ? ",(500,0))

id_ = 1
for i in range(4):
    cursor.execute("DELETE FROM Users WHERE id = ?",(id_,))
    id_ += 3
connection.commit()
cursor.execute("SELECT * FROM Users")
list_ = cursor.fetchall()
for user in list_:
    print(f"Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}")

connection.close()
