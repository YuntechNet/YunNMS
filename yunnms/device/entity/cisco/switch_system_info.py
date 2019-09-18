from yunnms.device.entity import SystemInfo


class CiscoSwitchSystemInfo(SystemInfo):
    @staticmethod
    def polling(snmp_conn) -> "CiscoSwitchSystemInfo":
        outputs = snmp_conn.next(
            oids=[
                # System
                ("SNMPv2-MIB", "sysName"),
                ("SNMPv2-MIB", "sysDescr"),
                # CPU
                ("CISCO-PROCESS-MIB", "cpmCPUTotal5minRev"),
                ("CISCO-PROCESS-MIB", "cpmCPUTotal1minRev"),
                ("CISCO-PROCESS-MIB", "cpmCPUTotal5secRev"),
                # Memory
                ("CISCO-MEMORY-POOL-MIB", "ciscoMemoryPoolUsed"),
                ("CISCO-MEMORY-POOL-MIB", "ciscoMemoryPoolFree"),
            ]
        )
        return CiscoSwitchSystemInfo(
            system_name=outputs["SNMPv2-MIB::sysName.0"],
            system_description=outputs["SNMPv2-MIB::sysDescr.0"],
            cpu_5min=int(outputs["CISCO-PROCESS-MIB::cpmCPUTotal5minRev.1"]),
            cpu_1min=int(outputs["CISCO-PROCESS-MIB::cpmCPUTotal1minRev.1"]),
            cpu_5sec=int(outputs["CISCO-PROCESS-MIB::cpmCPUTotal5secRev.1"]),
            memory_used=int(outputs["CISCO-MEMORY-POOL-MIB::ciscoMemoryPoolUsed.1"]),
            memory_free=int(outputs["CISCO-MEMORY-POOL-MIB::ciscoMemoryPoolFree.1"]),
        )

    def __init__(
        self,
        system_name: str,
        system_description: str,
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
            system_name=system_name,
            system_description=system_description,
            cpu_usage=cpu_5sec / 100,
            memory_usage=memory_used / (memory_free + memory_used),
        )
