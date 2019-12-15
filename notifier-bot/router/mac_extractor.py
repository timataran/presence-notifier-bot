import paramiko
from util import settings
import logging


class ActiveMacExtractor:

    @classmethod
    def get_list(cls):
        client = cls._get_ssh_client()

        router_settings = settings.get_router_settings()

        client.connect(
            router_settings['ip'],
            username=router_settings['username'],
            password=router_settings['password'],
            allow_agent=False,
            look_for_keys=False
        )
        stdin, stdout, stderr = client.exec_command('interface wireless registration-table print')

        connections = []
        for line in stdout:
            if ';;;' in line:
                continue
            connections.append(line[40:57])
        client.close()

        return connections[1:]

    @staticmethod
    def _get_ssh_client():
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.set_log_channel('ssh-client')
        logging.getLogger('ssh-client').setLevel(logging.WARNING)

        return client

