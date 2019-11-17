from os import getcwd
from os.path import join

from atomic_p2p.peer import ThreadPeer
from atomic_p2p.logging import getLogger
from atomic_p2p.utils.security import create_self_signed_cert as cssc, self_hash

from .role import Role
from .device import DeviceManager


class YunNMS(object):
    def __init__(
        self,
        addr: str,
        name: str,
        cert: str,
        ns: str = None,
        logger: "logging.Logger" = getLogger(__name__),
    ):
        cert_file, key_file = cssc(
            cert_dir=getcwd(), cert_file=cert, key_file=cert.replace(".pem", ".key")
        )
        addr = addr.split(":") if type(addr) is str else addr
        self.program_hash = self_hash(path=join(getcwd(), "yunnms"))

        self.peer = ThreadPeer(
            host=addr,
            name=name,
            role=Role.DEVICE,
            cert=(cert_file, key_file),
            program_hash=self.program_hash,
            ns=ns,
            logger=logger,
        )
        self.device_manager = DeviceManager(peer=self.peer, logger=logger)

    def start(self):
        self.peer.start()
        self.device_manager.start()
        if hasattr(self, "local_monitor"):
            getattr(self, "local_monitor").start()

    def stop(self):
        self.peer.stop()
        self.device_manager.stop()
        if hasattr(self, "local_monitor"):
            getattr(self, "local_monitor").stop()

    def _on_command(self, cmd):
        if type(cmd) != list and type(cmd) == str:
            cmd = cmd.strip().split(" ")

        service_key = cmd[0].lower()
        if service_key in ["peer", "monitor", "device"]:
            return (True, self.peer._on_command(cmd[1:]))
        elif service_key == "stop":
            self.stop()
            return (True, None)
        else:
            help_tips = (
                "peer help            - See peer's help\n"
                "monitor help        - See monitor's help\n"
                "exit/stop            - exit the whole program.\n"
            )
            return (True, help_tips)
