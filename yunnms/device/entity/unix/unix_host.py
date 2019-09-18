from typing import List

from yunnms.device.abc import DeviceABC
from yunnms.device.entity import SystemInfo
from yunnms.device.entity.device_type import DeviceType
from yunnms.device.entity import Interface


class UnixHost(DeviceABC):
    @staticmethod
    def snmp_polling(ip: str, snmp_conn: "SNMPConnectionABC") -> "UnixHost":
        return UnixHost(
            ip=ip,
            system_info=SystemInfo.snmp_polling(snmp_conn=snmp_conn),
            interfaces=Interface.snmp_polling(snmp_conn=snmp_conn),
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
