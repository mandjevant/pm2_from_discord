import spur
import os

on_message_users = {204184798200201216: r'.*(pim|076 | 076|204184798200201216|terminator076|terminator)\b.*'}
path = os.path.dirname(os.path.abspath(__file__))
av_users = """Pim dankmemes | parameter: `pim`
Bot-Daemon | parameter: `daemon` NOT WORKING
Pim main dm AWS | parameter: `pimaws`
Batman AWS | parameter: `batmanaws`
Catfish AWS | parameter: `catfishaws`"""


def create_conn(hostname, username, private_key_file):
    shell = spur.SshShell(
        hostname=hostname,
        username=username,
        private_key_file=path+private_key_file,
        missing_host_key=spur.ssh.MissingHostKey.accept
    )

    return shell
