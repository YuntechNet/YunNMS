from typing import List, Dict

from ...abc.device import DeviceABC
from ...abc.snmp import SNMPPollABC, SNMPTrapABC
from .. import DeviceType
from ..inet import Interface
from .switch_system_info import CiscoSwitchSystemInfo


class CiscoSwitch(DeviceABC, SNMPPollABC, SNMPTrapABC):
    @staticmethod
    def new(ip: str, snmp_conn: "SNMPConnectionABC") -> "CiscoSwitch":
        return CiscoSwitch(
            ip=ip,
            system_info=CiscoSwitchSystemInfo.new(snmp_conn=snmp_conn),
            interfaces=Interface.new_interfaces(snmp_conn=snmp_conn),
        )

    def __init__(
        self, ip: str, system_info: "SystemInfo", interfaces: List["Interface"]
    ) -> None:
        super().__init__(
            ip=ip,
            device_type=DeviceType.CiscoSwitch,
            system_info=system_info,
            interfaces=interfaces,
        )

    def snmp_poll(self, snmp_conn: "SNMPConnectionABC") -> List[object]:
        return [
            self.system_info.snmp_poll(snmp_conn=snmp_conn),
            [each.snmp_poll(snmp_conn=snmp_conn) for each in self.interfaces],
        ]

    def poll_update(self, snmp_conn: "SNMPConnectionABC") -> None:
        self.system_info.poll_update(snmp_conn=snmp_conn)
        for each in self.interfaces:
            each.poll_update(snmp_conn=snmp_conn)

    def is_trap_match(self, context: Dict, result: Dict[str, str]) -> bool:
        return context["transportAddress"][0] == self.ip

    def trap_update(self, context: Dict, result: Dict) -> None:
        for each in self.interfaces:
            if each.is_trap_match(context=context, result=result) is True:
                return each.trap_update(context=context, result=result)

    def update(self) -> None:
        pass
