from pysnmp.hlapi.asyncore import SnmpEngine

from atomic_p2p.peer import Peer
from atomic_p2p.utils.manager import ProcManager
from atomic_p2p.utils.logging import getLogger

from .command import HelpCmd, AddCmd, RemoveCmd, ListCmd
from .trap_server import TrapServer


class DeviceManager(ProcManager):

    def __init__(self, peer, loop_delay=60):
        self.peer = peer
        super(DeviceManager, self).__init__(
            loopDelay=loop_delay, auto_register=True,
            logger=getLogger(__name__))
        self.devices = []
        self._snmp_engine = SnmpEngine()
        # self.trap_server = TrapServer()

    def _register_handler(self):
        pass

    def _register_command(self):
        self.commands = {
            'help': HelpCmd(self),
            'add': AddCmd(self),
            'remove': RemoveCmd(self),
            'list': ListCmd(self)
        }

    def onProcess(self, msg_arr, **kwargs):
        try:
            msg_key = msg_arr[0].lower()
            msg_arr = msg_arr[1:]
            if msg_key in self.commands:
                return self.commands[msg_key]._on_process(msg_arr)
            return self.commands['help']._on_process(msg_arr)
        except Exception as e:
            return self.commands['help']._on_process(msg_arr)

    def start(self):
        super(DeviceManager, self).start()
        # self.trap_server.start()    # L18

    def stop(self):
        super(DeviceManager, self).stop()
        # self.trap_server.stop()     # L18

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            pass

    def addDevice(self, device):
        if type(device) is Device and device not in self.devices:
            self.devices.append(device)
            if device.connect_type == 'snmp':
                device.snmp_v3_init()
            else:
                device.fetch_running_config()
                device.fetch_interface_status()
