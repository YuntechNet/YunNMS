from atomic_p2p.utils.communication import Handler, Packet


class SyncHandler(Handler):
    pkt_type = "device_sync"

    def __init__(self, peer):
        super(SyncHandler, self).__init__(peer=peer, pkt_type=type(self).pkt_type)

    def on_send_pkt(self, target, device):
        return Packet(
            dst=target,
            src=self.peer.server_info.host,
            program_hash=self.peer.program_hash,
        )

    def on_recv_pkt(self):
        pass
