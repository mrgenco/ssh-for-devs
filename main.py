import click
import paramiko

@click.command()
@click.option('--host', prompt='Enter the hostname', help='Remote host to connect to')
@click.option('--username', prompt='Enter your username', help='Your SSH username')
@click.option('--password', prompt='Enter your password', hide_input=True, help='Your SSH password')
def cli(host, username, password):
    """This is a simple SSH client application designed for developers"""
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
        print("Authentication failed, please check your credentials.")
    except paramiko.SSHException as e:
        print("Unable to establish SSH connection:", str(e))
    finally:
        ssh.close()

if __name__ == '__main__':
    cli()
