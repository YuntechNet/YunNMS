from yunnms.device.abc import SNMPPollingABC


class SystemInfo(SNMPPollingABC):
    @staticmethod
    def snmp_polling(snmp_conn: "SNMPConnectionABC") -> "SystemInfo":
        outputs = snmp_conn.next(
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
        return SystemInfo(
            system_name=outputs["SNMPv2-MIB::sysName.0"],
            system_description=outputs["SNMPv2-MIB::sysDescr.0"],
            cpu_usage=int(outputs["UCD-SNMP-MIB::ssCpuSystem.0"]) / 100,
            memory_usage=1
            - (
                int(outputs["UCD-SNMP-MIB::memAvailReal.0"])
                / int(outputs["UCD-SNMP-MIB::memTotalReal.0"])
            ),
        )

    def __init__(
        self,
        system_name: str,
        system_description: str,
        cpu_usage: float,
        memory_usage: float,
    ) -> None:
        self.system_name = system_name
        self.system_description = system_description
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage

    def __str__(self) -> str:
        return "{}<CPU_USE: {}, MEM_USE: {}>".format(
            type(self).__name__, self.cpu_usage, self.memory_usage
        )

    def __repr__(self) -> str:
        return self.__str__()
