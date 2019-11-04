from typing import Dict, List

from yunnms.device.entity import SystemInfo


class CiscoSwitchSystemInfo(SystemInfo):
    @staticmethod
    def new(snmp_conn: "SNMPConnectionABC") -> "CiscoSwitchSystemInfo":
        system_info = CiscoSwitchSystemInfo(None, None, 100, 100, 100, 100, 100)
        system_info.poll_update(snmp_conn=snmp_conn)
        return system_info

    def __init__(
        self,
        name: str,
        description: str,
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
            name=name,
            description=description,
            cpu_usage=cpu_5min,
            memory_usage=(memory_used / (memory_free + memory_used)) * 100,
        )

    def calculate(self):
        self.cpu_usage = self.cpu_5min
        self.memory_usage = (
            self.memory_used / (self.memory_free + self.memory_used)
        ) * 100

    def snmp_poll(self, snmp_conn: "SNMPConnectionABC") -> List[object]:
        output = snmp_conn.next(
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
        return [
            output["SNMPv2-MIB::sysName.0"],
            output["SNMPv2-MIB::sysDescr.0"],
            int(output["CISCO-PROCESS-MIB::cpmCPUTotal5minRev.1"]),
            int(output["CISCO-PROCESS-MIB::cpmCPUTotal1minRev.1"]),
            int(output["CISCO-PROCESS-MIB::cpmCPUTotal5secRev.1"]),
            int(output["CISCO-MEMORY-POOL-MIB::ciscoMemoryPoolUsed.1"]),
            int(output["CISCO-MEMORY-POOL-MIB::ciscoMemoryPoolFree.1"]),
        ]

    def poll_update(self, snmp_conn: "SNMPConnectionABC") -> None:
        name, description, cpu_5min, cpu_1min, cpu_5sec, memory_used, memory_free = self.snmp_poll(
            snmp_conn=snmp_conn
        )
        self.name = name
        self.description = description
        self.cpu_5min = cpu_5min
        self.cpu_1min = cpu_1min
        self.cpu_5sec = cpu_5sec
        self.memory_used = memory_used
        self.memory_free = memory_free
        self.calculate()
