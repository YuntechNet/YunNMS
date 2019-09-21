from typing import List

from yunnms.device.abc import DeviceABC, SNMPPollingABC
from yunnms.device.entity import SystemInfo
from yunnms.device.entity.device_type import DeviceType
from yunnms.device.entity import Interface


class UnixHost(DeviceABC, SNMPPollingABC):
    @staticmethod
    def new(ip: str, snmp_conn: "SNMPConnectionABC") -> "UnixHost":
        return UnixHost(
            ip=ip,
            snmp_conn=snmp_conn,
            system_info=SystemInfo.new(snmp_conn=snmp_conn),
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
            device_type=DeviceType.UnixHost,
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
