import sqlite3

connection = sqlite3.connect('not_telegram.db')
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
# cursor.execute("UPDATE Users SET balance = ? WHERE id%2 != ? ",(500,0))
#
# id_ = 1
# for i in range(4):
#     cursor.execute("DELETE FROM Users WHERE id = ?",(id_,))
#     id_ += 3
# cursor.execute("DELETE FROM Users WHERE id = ?",(6,))
cursor.execute("SELECT COUNT(*) FROM Users")
total = cursor.fetchone()[0]
cursor.execute("SELECT SUM(balance) FROM Users")
sum_ = cursor.fetchone()[0]
cursor.execute("SELECT AVG(balance) FROM Users")
avg_ = cursor.fetchone()[0]
print(f"Количество записей {total}, Сумма балансов {sum_}, Средная сумма {sum_/total} или через SQL {avg_}")
connection.commit()
connection.close()