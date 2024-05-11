import sqlite3


# **Создайте подключение к базе данных**:
connection = sqlite3.connect('test_database.db')

# **Создайте объект cursor для выполнения SQL команд**:
cursor = connection.cursor()

# **Создайте таблицу**:
cursor.execute('''
CREATE TABLE 
IF NOT EXISTS users (
id INTEGER PRIMARY KEY, 
name TEXT, 
age INTEGER)
''')

# **Добавьте данные**:
cursor.execute('''
INSERT INTO users (
name, 
age
) 
VALUES (
'Это пробная запись', 
1
)''')
connection.commit()

# **Запросите данные**:
cursor.execute('''
SELECT * FROM users
''')
rows = cursor.fetchall()
for row in rows:
    print(row)

# **Закройте подключение**:
connection.close()
