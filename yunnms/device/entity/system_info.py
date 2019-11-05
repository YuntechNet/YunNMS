from typing import Union, List, Dict

from yunnms.device.abc import SNMPPollABC


class SystemInfo(SNMPPollABC):
    @staticmethod
    def new(snmp_conn: "SNMPConnectionABC", *args, **kwargs) -> "SystemInfo":
        system_info = SystemInfo(None, None, 0.0, 0.0)
        system_info.poll_update(snmp_conn=snmp_conn)
        return system_info

    def __init__(
        self, name: str, description: str, cpu_usage: float, memory_usage: float
    ) -> None:
        self.name = name
        self.description = description
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage

    def snmp_poll(
        self, snmp_conn: "SNMPConnectionABC", *args, **kwargs
    ) -> List[object]:
        output = snmp_conn.next(
            oids=[
                # System
                ("SNMPv2-MIB", "sysName"),
                ("SNMPv2-MIB", "sysDescr"),
                # CPU
                ("UCD-SNMP-MIB", "ssCpuSystem"),
                # Memory
                ("UCD-SNMP-MIB", "memTotalReal"),
                ("UCD-SNMP-MIB", "memAvailReal"),
            ]
        )
        return [
            output["SNMPv2-MIB::sysName.0"],
            output["SNMPv2-MIB::sysDescr.0"],
            int(output["UCD-SNMP-MIB::ssCpuSystem.0"]) / 100,
            1
            - (
                int(output["UCD-SNMP-MIB::memAvailReal.0"])
                / int(output["UCD-SNMP-MIB::memTotalReal.0"])
            ),
        ]

    def poll_update(self, snmp_conn: "SNMPConnectionABC", *args, **kwargs) -> None:
        name, description, cpu_usage, memory_usage = self.snmp_poll(snmp_conn=snmp_conn)
        self.name = name
        self.description = description
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage

    def __str__(self) -> str:
        return "{}<CPU_USE: {:2.02f}%, MEM_USE: {:2.02f}%>".format(
            type(self).__name__, self.cpu_usage, self.memory_usage
        )

    def __repr__(self) -> str:
        return self.__str__()
