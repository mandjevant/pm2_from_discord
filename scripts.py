import spur
import os

# Populate as {discordID: regex, discordID: regex}
on_message_users = {}
path = os.path.dirname(os.path.abspath(__file__))


def create_conn(hostname, username, private_key_file):
    shell = spur.SshShell(
        hostname=hostname,
        username=username,
        private_key_file=path+private_key_file,
        missing_host_key=spur.ssh.MissingHostKey.accept
    )

    return shell
