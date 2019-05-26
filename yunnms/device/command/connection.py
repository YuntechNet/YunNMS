from atomic_p2p.utils.command import Command

from ..connection import SSHConnection, TelnetConnection


class ConnectionCmd(Command):
    """
        Command to modified connections of a device.
        Usage in prompt:
            device [connection/conn]
    """

    def __init__(self, device):
        super(ConnectionCmd, self).__init__('connection')
        self.device = device
        self.peer = device.peer
        self.commands = {
            'add': AddCmd(self.device)
        }

    def onProcess(self, msg_arr, **kwargs):
        try:
            msg_key = msg_arr[0].lower()
            msg_arr = msg_arr[1:]
            if msg_key in ['add']:
                return self.commands[msg_key]._on_process(msg_arr)
            return self.commands['help']._on_process(msg_arr)
        except Exception as e:
            return self.commands['help']._on_process(msg_arr)


class AddCmd(Command):
    """
        Command to add a new connection.
        Usage in prompt:
            device [connection/conn] add device_name [ssh/telnet]ip:port
             account password
    """

    def __init__(self, device):
        super(AddCmd, self).__init__('connection.add')
        self.device = device
        self.peer = device.peer

    def onProcess(self, msg_arr):
        device_name = msg_arr[0]
        if device_name not in self.device._devices:
            return '{} not exists'.format(device_name)

        device = self.device._devices[device_name]
        conn_type = msg_arr[1]
        if conn_type == 'ssh':
            host = msg_arr[2].split(':')
            ssh_conn = SSHConnection(authentication={
                'host': (host[0], host[1]),
                'account': msg_arr[3],
                'password': msg_arr[4]
            })
            device.set_ssh_conn(ssh_conn=ssh_conn)
            return '{} added ssh connection.'.format(str(device))
        elif conn_type == 'telnet':
            host = msg_arr[2].split(':')
            telnet_conn = TelnetConnection(authentication={
                'host': (host[0], host[1]),
                'account': msg_arr[3],
                'password': msg_arr[4]
            })
            device.set_telnet_conn(telnet_conn=telnet_conn)
            return '{} added telnet connection.'.format(str(device))
        return 'Add failed with connection type {}.'.format(conn_type)
