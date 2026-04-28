import sqlite3

DB_NAME = "email_history.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 🔹 EXISTING TABLE (UNCHANGED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        category TEXT,
        sentiment TEXT,
        priority TEXT
    )
    """)

    # 🔹 NEW TABLE (USERS SYSTEM)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    conn.commit()
    conn.close()
