from typing import List

from yunnms.device.abc import DeviceABC, SNMPPollingABC
from yunnms.device.entity.device_type import DeviceType
from yunnms.device.entity.inet import Interface

from .switch_system_info import CiscoSwitchSystemInfo


class CiscoSwitch(DeviceABC, SNMPPollingABC):
    @staticmethod
    def new(ip: str, snmp_conn: "SNMPConnectionABC") -> "CiscoSwitch":
        return CiscoSwitch(
            ip=ip,
            snmp_conn=snmp_conn,
            system_info=CiscoSwitchSystemInfo.new(snmp_conn=snmp_conn),
            interfaces=Interface.new(snmp_conn=snmp_conn),
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

    def snmp_polling(self, snmp_conn: "SNMPConnectionABC") -> None:
        self.system_info.snmp_polling(snmp_conn=self.snmp_conn)
        # Not polling each Interface.
        # for each in self.interfaces:
        #     each.snmp_polling(snmp_conn=self.snmp_conn)

    def update(self) -> None:
        self.snmp_polling(snmp_conn=self.snmp_conn)
