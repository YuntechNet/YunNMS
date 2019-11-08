from typing import Tuple
from enum import IntEnum

from atomic_p2p.utils.communication import Handler, Packet

from ..entity import DeviceType
from ..entity.unix import UnixHost
from ..entity.cisco import CiscoSwitch


class SyncAction(IntEnum):
    UPDATE = 0x00
    DELETE = 0x01
    INSERT = 0x02


class SyncHandler(Handler):
    pkt_type = "device_sync"

    def __init__(self, device_manager: "DeviceManager") -> None:
        super().__init__(peer=device_manager.peer, pkt_type=type(self).pkt_type)
        self.manager = device_manager

    def on_send_pkt(
        self, target: Tuple[str, int], act: "SyncAction", device: "DeviceABC"
    ) -> "Packet":
        data = {"act": act, "device": type(device).serilizable(obj=device)}
        return Packet(
            dst=target,
            src=self.peer.server_info.host,
            program_hash=self.peer.program_hash,
            _type=type(self).pkt_type,
            _data=data,
        )

    def on_recv_pkt(
        self, src: Tuple[str, int], pkt: "Packet", conn: "SSLSocket", **kwargs
    ) -> None:
        act = SyncAction(pkt.data["act"])
        device_data = pkt.data["device"]
        name = device_data["system_info"]["name"]
        if act == SyncAction.UPDATE:
            self.manager.update_device(name=name, data=device_data)
        elif act == SyncAction.DELETE:
            self.manager.remove_device(name=name, data=device_data)
        elif act == SyncAction.INSERT:
            if DeviceType(device_data["device_type"]) == DeviceType.UnixHost:
                self.manager.add_device(device=UnixHost(**device_data))
            elif DeviceType(device_data["device_type"]) == DeviceType.CiscoSwitch:
                self.manager.add_device(device=CiscoSwitch(**device_data))
