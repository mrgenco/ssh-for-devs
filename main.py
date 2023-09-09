import click
import paramiko
from db import create_tables
from db import insert_connection
from db import get_connections


@click.command()
@click.option('--name', prompt='Enter a name(label) for your connection', help='Remote host to connect to')
@click.option('--host', prompt='Enter the hostname', help='Remote host to connect to')
@click.option('--username', prompt='Enter your username', help='Your SSH username')
@click.option('--password', prompt='Enter your password', hide_input=True, help='Your SSH password')
def add_connection(name, host, username, password):
    
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh.connect(name, host, username, password)


        while True:
            command = input(f'{username}@{host}$ ')
            if command.lower() == 'exit':
                break

            # Execute the command
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            click.echo(output)


    except paramiko.AuthenticationException:
        click.echo("Authentication failed, please check your credentials.")
    except paramiko.SSHException as e:
        click.echo("Unable to establish SSH connection:", str(e))
    except Exception as e:
        click.echo("Exception occured while adding new SSH connection:", str(e))
    finally:
        # Save the connection information for later usage
        insert_connection(name, host, username, password)
        ssh.close()


def connect(host, username, password):
    click.echo(f'Connecting to {username}@{host}...')
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote server
    ssh.connect(host, username, password)

    while True:
        command = input(f'{username}@{host}$ ')
        if command.lower() == 'exit':
            break

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        click.echo(output)


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

    
    
    

@click.command()
@click.option('--add', 'action', flag_value='add', help='Add new connection')
@click.option('--show', 'action', flag_value='show',help='Show connections')
def main(action):
    if(action == 'add'):
        add_connection()
    if(action == 'show'):
        show_connections()
    else:
        click.echo('Invalid usage of ssh-for-dev. Use --help for available options')

if __name__ == '__main__':
    create_tables()
    main()
