from typing import List

from yunnms.device.abc import SNMPv3PollingAbc
from yunnms.device.entity.device_type import DeviceType
from yunnms.device.entity.device_v2 import Device
from yunnms.device.entity.inet import Interface

from .switch_system_info import CiscoSwitchSystemInfo


class CiscoSwitch(Device, SNMPv3PollingAbc):
    @staticmethod
    def polling(ip: str, snmp_conn: "SNMPv3Connection") -> "CiscoSwitch":
        return CiscoSwitch(
            ip=ip,
            snmp_conn=snmp_conn,
            system_info=CiscoSwitchSystemInfo.polling(snmp_conn=snmp_conn),
            interfaces=Interface.polling(snmp_conn=snmp_conn),
        )

    def __init__(
        self,
        ip: str,
        snmp_conn: "SNMPv3Connection",
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
