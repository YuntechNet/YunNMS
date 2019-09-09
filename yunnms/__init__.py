from os import getcwd
from os.path import join

from atomic_p2p.peer import ThreadPeer
from atomic_p2p.utils.logging import getLogger
from atomic_p2p.utils.security import create_self_signed_cert as cssc, self_hash

from .role import Role
from .device import DeviceManager


class YunNMS(object):
    def __init__(self, addr: str, name: str, cert: str, ns: str = None):
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
            logger=getLogger(__name__),
        )
        self.device_manager = DeviceManager(peer=self.peer)

    def start(self):
        self.peer.start()
        # self.device_manager.start()

    def stop(self):
        self.peer.stop()
        # self.device_manager.stop()
