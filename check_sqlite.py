import sqlite3


# Проверяем версию SQLite
print("SQLite version:", sqlite3.sqlite_version)

# Проверяем, может ли Python подключиться к SQLite
try:
    conn = sqlite3.connect(":memory:")  # Создаем временную базу в памяти
    cursor = conn.cursor()
    cursor.execute("SELECT 1 + 1")
    result = cursor.fetchone()
    print("SQLite работает! Результат тестового запроса:", result[0])
    conn.close()
except Exception as e:
    print("Ошибка подключения к SQLite:", e)
