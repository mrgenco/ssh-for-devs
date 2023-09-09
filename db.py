import sqlite3

# Create a SQLite database (or connect to an existing one)
conn = sqlite3.connect('connections.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY,
            name TEXT,
            host TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()

def insert_connection(name, host, username, password):
    cursor.execute("INSERT INTO connections (name, host, username, password) VALUES (?, ?, ?, ?)", (name, host, username, password))
    conn.commit()

def get_connections():
    cursor.execute("SELECT id, name, host, username, password FROM connections")
    return cursor.fetchall()