import click
import paramiko
from db import create_tables
from db import insert_connection
from db import get_connections


@click.command()
@click.option('--host', prompt='Enter the hostname', help='Remote host to connect to')
@click.option('--username', prompt='Enter your username', help='Your SSH username')
@click.option('--password', prompt='Enter your password', hide_input=True, help='Your SSH password')
def add_connection(host, username, password):
    
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh.connect(host, username=username, password=password)

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
    finally:
        ssh.close()


def edit_connection():
    # Implement editing logic here
    pass

def show_connections():
    connections = get_connections()
    

@click.command()
@click.option('--add', 'action', flag_value='add')
@click.option('--show', 'action', flag_value='show', default=True)
def main(action):
    click.echo(action)
    
    if(action == 'add'):
        add_connection()
    if(action == 'show'):
        show_connections()

if __name__ == '__main__':
    create_tables()
    main()
