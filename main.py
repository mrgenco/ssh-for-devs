import sqlite3
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

# Create a SQLite database (or connect to an existing one)
conn = sqlite3.connect('connections.db')
cursor = conn.cursor()

# Create a table to store connection details
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

def add_connection():
    print("add_connection invoked")
    name = prompt("Connection Name: ")
    host = prompt("Host: ")
    username = prompt("Username: ")
    password = prompt("Password: ", is_password=True)

    cursor.execute("INSERT INTO connections (name, host, username, password) VALUES (?, ?, ?, ?)", (name, host, username, password))
    conn.commit()
    print("Connection added successfully.")

def edit_connection():
    # Implement editing logic here
    pass

def show_connections():
    cursor.execute("SELECT id, name, host FROM connections")
    connections = cursor.fetchall()

    connection_completer = WordCompleter([f"{conn[0]}: {conn[1]} ({conn[2]})" for conn in connections])

    selected_connection = select_menu([f"{conn[0]}: {conn[1]} ({conn[2]})" for conn in connections], title="Select a connection to connect to: ", menu_cursor=8)

    # Implement connection logic based on the selected_connection
    pass

def main():
    result = radiolist_dialog(
        title="SSH dialog",
        text="Which action you want to take?",
        values=[
            ("add", "Add New Connection"),
            ("edit", "Edit Connection"),
            ("show", "Show Connections")
        ]
    ).run()

    
    print(f"Result = {result}")
    add_connection()

if __name__ == '__main__':
    main()
