from typing import Union, List, Dict

from yunnms.device.abc import SNMPPollingABC


class SystemInfo(SNMPPollingABC):
    @staticmethod
    def new(snmp_conn: "SNMPConnectionABC") -> "SystemInfo":
        system_info = SystemInfo(None, None, 100, 100)
        system_info.snmp_polling(snmp_conn=snmp_conn)
        return system_info

    def __init__(
        self, name: str, description: str, cpu_usage: float, memory_usage: float
    ) -> None:
        self.name = name
        self.description = description
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage

    def snmp_polling(self, snmp_conn: "SNMPConnectionABC") -> Union[List, Dict]:
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
        self.name = output["SNMPv2-MIB::sysName.0"]
        self.description = output["SNMPv2-MIB::sysDescr.0"]
        self.cpu_usage = int(output["UCD-SNMP-MIB::ssCpuSystem.0"]) / 100
        self.memory_usage = 1 - (
            int(output["UCD-SNMP-MIB::memAvailReal.0"])
            / int(output["UCD-SNMP-MIB::memTotalReal.0"])
        )

    def __str__(self) -> str:
        return "{}<CPU_USE: {:2.02f}%, MEM_USE: {:2.02f}%>".format(
            type(self).__name__, self.cpu_usage, self.memory_usage
        )

    def __repr__(self) -> str:
        return self.__str__()
