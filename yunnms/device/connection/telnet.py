from telnetlib import Telnet, IAC, NOP


class TelnetConnection(object):

    def __init__(self, authentication, debug_level=0):
        self.host = authentication['host']
        self.username = authentication['account']
        self.password = authentication['password']
        self.debug_level = debug_level

    def login(self, debug_level=None):
        debug_level = debug_level if debug_level else self.debug_level
        self.client = Telnet(host=self.host[0], port=self.host[1])
        self.client.set_debuglevel(debug_level)
        if self.username:
            self.client.read_until(bytes('login:', encoding='utf-8'))
            self.client.write(bytes(self.username + '\n', encoding='utf-8'))
        self.client.read_until(bytes('Password', encoding='utf-8'))
        self.client.write(bytes(self.password + '\n', encoding='utf-8'))
        return self

    def sendCommand(self, command, wrap=True):
        self.client.write(bytes(command + ('\n' if wrap else ''),
                                encoding='utf-8'))

    def logout(self):
        if self.client:
            self.client.close()

    def is_active(self):
        try:
            if self.client.sock:
                self.client.sock.send(IAC + NOP)
                self.client.sock.send(IAC + NOP)
                self.client.sock.send(IAC + NOP)
                return True
        except Exception as e:
            pass
        return False
