from threading import Thread, Event as tEvent

from pysnmp.hlapi.asyncore import SnmpEngine

from atomic_p2p.peer import Peer

from yunnms.role import Role
from .entity import Device
from .communication import SyncHandler
from .command import HelpCmd, RemoveCmd, ListCmd, NewCmd, ConnectionCmd
from .snmp import TrapServer


class DeviceManager(Thread):
    def __init__(self, peer: "Peer", loop_delay: int = 60):
        super(DeviceManager, self).__init__()
        self.loop_delay = loop_delay
        self.stopped = tEvent()
        self.started = tEvent()

        self.peer = peer
        self._register_handler()
        self._register_command()

        self._devices = {}
        self._snmp_engine = SnmpEngine()
        # self.trap_server = TrapServer()

    def start(self):
        self.started.set()
        super(DeviceManager, self).start()
        # self.trap_server.start()    # L18

    def stop(self):
        self.stopped.set()
        self.started.clear()
        # self.trap_server.stop()     # L18

    def run(self):
        while self.stopped.wait(self.loop_delay) is False:
            pass

    def add_device(self, name, device):
        if type(device) is Device and name not in self._devices:
            self._devices[name] = device

    def _register_handler(self):
        installing_handler = [SyncHandler(self)]
        for each in installing_handler:
            self.peer.register_handler(handler=each)

    def _register_command(self):
        installing_commands = [
            HelpCmd(self),
            RemoveCmd(self),
            ListCmd(self),
            NewCmd(self),
            ConnectionCmd(self),
        ]
        for each in installing_commands:
            self.peer.register_command(command=each)
