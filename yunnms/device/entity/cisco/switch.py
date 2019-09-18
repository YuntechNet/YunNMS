from typing import List

from yunnms.device.abc import DeviceABC, SNMPPollingABC
from yunnms.device.entity.device_type import DeviceType
from yunnms.device.entity.inet import Interface

from .switch_system_info import CiscoSwitchSystemInfo


class CiscoSwitch(DeviceABC, SNMPPollingABC):
    @staticmethod
    def snmp_polling(ip: str, snmp_conn: "SNMPConnectionABC") -> "CiscoSwitch":
        return CiscoSwitch(
            ip=ip,
            snmp_conn=snmp_conn,
            system_info=CiscoSwitchSystemInfo.snmp_polling(snmp_conn=snmp_conn),
            interfaces=Interface.snmp_polling(snmp_conn=snmp_conn),
        )

    def __init__(
        self,
        ip: str,
        snmp_conn: "SNMPConnectionABC",
        system_info: "SystemInfo",
        interfaces: List["Interface"],
    ) -> None:
        super().__init__(
            ip=ip,
            device_type=DeviceType.CiscoSwitch,
            system_info=system_info,
            interfaces=interfaces,
        )
        self.snmp_conn = snmp_conn

    def update(self) -> None:
        pass
