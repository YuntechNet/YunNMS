from typing import Tuple
from logging import getLogger

from pysnmp.hlapi.asyncore import SnmpEngine
from atomic_p2p.utils.manager import ThreadManager
from atomic_p2p.peer import ThreadPeer

from yunnms.role import Role
from yunnms.device.abc import DeviceABC
from .communication import SyncHandler
from .command import HelpCmd, RemoveCmd, ListCmd, NewCmd, ConnectionCmd
from .trap_server import TrapServer


class DeviceManager(ThreadManager):
    def __init__(
        self,
        peer: "Peer",
        trap_host: Tuple[str, int] = ("0.0.0.0", 162),
        loop_delay: int = 60,
        logger=getLogger(),
    ):
        super().__init__(loopDelay=loop_delay, logger=logger)
        self.peer = peer
        self._register_handler()
        self._register_command()

        self._devices = {}
        self._snmp_engine = SnmpEngine()
        self.trap_server = TrapServer(host=trap_host)

    def start(self):
        super().start()
        self.trap_server.start()

    def stop(self):
        super().stop()
        self.trap_server.stop()

    def run(self):
        while self.stopped.wait(self.loopDelay) is False:
            for (_, device) in self._devices.items():
                device.update()

    def add_device(self, name, device):
        if isinstance(device, DeviceABC) and name not in self._devices:
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
