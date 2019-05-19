from time import sleep
from paramiko import SSHClient, AutoAddPolicy


class SSHConnection(object):

    def __init__(self, authentication, timeout=60):
        self.host = (authentication['host'][0], int(authentication['host'][1]))
        self.username = authentication['account']
        self.password = authentication['password']
        self.timeout = timeout

        self.client, self.shell, self.output = None, None, None

    def login(self, timeout=None):
        self.timeout = timeout if timeout is not None else self.timeout
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(hostname=self.host[0], port=self.host[1],
                            username=self.username, password=self.password,
                            timeout=self.timeout, look_for_keys=False,
                            allow_agent=False)
        self.shell = self.client.invoke_shell()
        self.output = self.shell.recv(65535)
        return self

    def logout(self):
        if self.client:
            self.client.close()

    def send_command(self, command, wrap=True, time_sleep=0.5, short=True):
        self.shell.send(str(command) + ('\n' if wrap else ''))
        sleep(time_sleep)
        output = self.shell.recv(65535).decode('utf-8')
        while ('#' not in output and '>' not in output):
            if ' --More-- ' in output:
                output = output.replace(' --More-- ', '') + \
                         self.send_command(command='q' if short else ' ',
                                           wrap=False, time_sleep=time_sleep,
                                           short=short)
            elif self.is_active():
                output += self.shell.recv(65535).decode('utf-8')
            else:
                break
        self.output = output
        return self.output

    def send_commands(self, commands, wrap=True, time_sleep=0.5, short=True):
        if type(commands) == list:
            output = ''
            for each in commands:
                output += self.send_command(
                                command=each, wrap=wrap, time_sleep=time_sleep,
                                short=short)
            return output
        else:
            return self.send_command(command=commands, wrap=wrap,
                                     time_sleep=time_sleep)

    def is_active(self):
        if self.client and self.client.get_transport():
            return self.client.get_transport().is_active()
        return False
