from typing import List, Dict

from yunnms.device.abc import DeviceABC, SNMPPollABC, SNMPTrapABC
from yunnms.device.entity import SystemInfo
from yunnms.device.entity.device_type import DeviceType
from yunnms.device.entity import Interface


class UnixHost(DeviceABC, SNMPPollABC, SNMPTrapABC):
    @staticmethod
    def new(ip: str, snmp_conn: "SNMPConnectionABC") -> "UnixHost":
        return UnixHost(
            ip=ip,
            snmp_conn=snmp_conn,
            system_info=SystemInfo.new(snmp_conn=snmp_conn),
            interfaces=Interface.new_interfaces(snmp_conn=snmp_conn),
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

    def snmp_poll(self, snmp_conn: "SNMPConnectionABC") -> List[object]:
        return [
            self.system_info.snmp_poll(snmp_conn=self.snmp_conn),
            [each.snmp_poll(snmp_conn=self.snmp_conn) for each in self.interfaces],
        ]

    def poll_update(self, snmp_conn: "SNMPConnectionABC") -> None:
        self.system_info.poll_update(snmp_conn=snmp_conn)
        for each in self.interfaces:
            each.poll_update(snmp_conn=snmp_conn)

    def is_trap_match(self, context: Dict, result: Dict[str, str]) -> bool:
        return context["transportAddress"][0] == self.snmp_conn.host[0]

    def trap_update(self, context, result) -> None:
        for each in self.interfaces:
            if each.is_trap_match(context, result) is True:
                return each.trap_update(context=context, result=result)

    def update(self) -> None:
        self.snmp_poll(snmp_conn=self.snmp_conn)
