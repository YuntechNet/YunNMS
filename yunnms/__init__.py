from yunnms.device import DeviceManager


class YunNMS(object):

    def __init__(self, host, name, role):
        self.peer = Peer(host=host, name=name, role=role)
        self.device_manager = DeviceManager(peer=peer)
