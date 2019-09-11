from .snmp import SNMPv3PollingAbs


class SystemInfo(SNMPv3PollingAbs):
    @staticmethod
    def polling(snmp_conn) -> "SystemInfo":
        outputs = list(
            snmp_conn.next(
                oids=[
                    # CPU
                    ("UCD-SNMP-MIB", "ssCpuSystem"),
                    # Memory
                    ("UCD-SNMP-MIB", "memTotalReal"),
                    ("UCD-SNMP-MIB", "memAvailReal"),
                ]
            ).values()
        )
        return SystemInfo(
            cpu_usage=int(outputs[0]) / 100,
            memory_usage=1 - (int(outputs[2]) / int(outputs[1])),
        )

    def __init__(self, cpu_usage: float, memory_usage: float) -> None:
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage

    def __str__(self) -> str:
        return "{}<CPU_USE: {}, MEM_USE: {}>".format(
            type(self).__name__, self.cpu_usage, self.memory_usage
        )