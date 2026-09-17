import sqlite3

conn = sqlite3.connect("items.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    stock INTEGER,
    price INTEGER
)
""")



conn.commit()
conn.close()