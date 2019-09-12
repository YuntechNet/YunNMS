from typing import List

from yunnms.device.entity import SystemInfo
from yunnms.device.entity.device_type import DeviceType
from yunnms.device.entity.device_v2 import Device
from yunnms.device.entity import Interface


class UnixHost(Device):
    @staticmethod
    def polling(ip: str, snmp_conn: "SNMPv3Connection") -> "UnixHost":
        return UnixHost(
            ip=ip,
            system_info=SystemInfo.polling(snmp_conn=snmp_conn),
            interfaces=Interface.polling(snmp_conn=snmp_conn),
        )

    def __init__(
        self, ip: str, system_info: "SystemInfo", interfaces: List["Interface"]
    ) -> None:
        super().__init__(
            ip=ip,
            device_type=DeviceType.UnixHost,
            system_info=system_info,
            interfaces=interfaces,
        )

    def update(self) -> None:
        pass
