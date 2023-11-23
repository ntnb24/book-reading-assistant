# app/database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Write a SQL query to create a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()