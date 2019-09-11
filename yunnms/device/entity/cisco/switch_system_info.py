from yunnms.device.entity import SystemInfo


class CiscoSwitchSystemInfo(SystemInfo):
    @staticmethod
    def polling(snmp_conn) -> "CiscoSwitchSystemInfo":
        return CiscoSwitchSystemInfo(
            *[
                int(each)
                for each in snmp_conn.next(
                    oids=[
                        # CPU
                        ("CISCO-PROCESS-MIB", "cpmCPUTotal5minRev"),
                        ("CISCO-PROCESS-MIB", "cpmCPUTotal1minRev"),
                        ("CISCO-PROCESS-MIB", "cpmCPUTotal5secRev"),
                        # Memory
                        ("CISCO-MEMORY-POOL-MIB", "ciscoMemoryPoolUsed"),
                        ("CISCO-MEMORY-POOL-MIB", "ciscoMemoryPoolFree"),
                    ]
                ).values()
            ]
        )

    def __init__(
        self,
        cpu_5min: int,
        cpu_1min: int,
        cpu_5sec: int,
        memory_used: int,
        memory_free: int,
    ) -> None:
        self.cpu_5min = cpu_5min
        self.cpu_1min = cpu_1min
        self.cpu_5sec = cpu_5sec
        self.memory_used = memory_used
        self.memory_free = memory_free
        super().__init__(
            cpu_usage=cpu_5sec / 100,
            memory_usage=memory_used / (memory_free + memory_used),
        )
