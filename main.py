from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from db import create_tables
from db import insert_connection
from db import get_connections



def add_connection():
    print("add_connection invoked")
    name = prompt("Connection Name: ")
    host = prompt("Host: ")
    username = prompt("Username: ")
    password = prompt("Password: ", is_password=True)

   
    insert_connection(name, host, username, password)
    print("Connection added successfully.")

def edit_connection():
    # Implement editing logic here
    pass

def show_connections():
    connections = get_connections()
    
    result = radiolist_dialog(
        title="Existing connection dialog",
        text="Pick the one you want to connect",
        values=[(str(i), label) for i, label in enumerate(connections)]
    ).run()

    print(f"Result = {result}")

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
    show_connections()

if __name__ == '__main__':
    create_tables()
    main()
