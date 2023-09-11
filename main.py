import click
import paramiko
import re
from db import create_tables
from db import insert_connection
from db import get_connections



@click.command()
@click.option('--add', 'action', flag_value='add', help='Add new connection')
@click.option('--show', 'action', flag_value='show',help='Show connections')
def main(action):
    if(action == 'add'):
        create_connection()
    if(action == 'show'):
        show_connections()
    else:
        show_connections()
       # click.echo('Invalid usage of ssh-for-dev. Use --help for available options')

import re  # Import the regular expressions library

def remove_ansi_escape_codes(text):
    # Use a regular expression to remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def create_connection():
    
    name = click.prompt('Enter a name(label) for your connection')
    host = click.prompt('Enter the hostname')
    username = click.prompt('Enter your username')
    password = click.prompt('Enter your password',hide_input=True)
    connect(host, username, password)
    # Save the connection information for later usage
    insert_connection(name, host, username, password)

  

def connect(host, username, password):

    try:
    
        click.echo(f'Connecting to {username}@{host}...')

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh.connect(hostname=host, port=22, username=username, password=password)

        # Open an interactive shell session
        ssh_shell = ssh.invoke_shell()     

        while True:
            # Get user input
            user_input = input()

            if user_input.lower() == 'exit':
                break

            # Send the user's command to the remote server
            ssh_shell.send(user_input + '\n')

            # Read and display the server's response
            response = ''
            while ssh_shell.recv_ready():
                response += ssh_shell.recv(1024).decode('utf-8')

            # Remove ANSI escape codes from the response
            clean_response = remove_ansi_escape_codes(response)
    
            print(clean_response)  
        
        # Close the shell session
        ssh_shell.close()

        # Close the SSH connection
        ssh.close()

        

    except paramiko.AuthenticationException:
        click.echo("Authentication failed, please check your credentials.")
    except paramiko.SSHException as e:
        click.echo("Unable to establish SSH connection:", str(e))
    except Exception as e:
        click.echo("Exception occured while adding new SSH connection:", str(e))
    finally:
        ssh.close()
    
    


def edit_connection():
    # Implement editing logic here
    pass


def show_connections():
    connections = get_connections()
    counter = 1
    for con in connections:
        print(counter,'. ' + con[1])
        counter = counter + 1
    connection_number = int(click.prompt('Enter the connection number'))
    connect(connections[connection_number - 1][2], connections[connection_number - 1][3], connections[connection_number - 1][4])

    
    

if __name__ == '__main__':
    create_tables()
    main()
