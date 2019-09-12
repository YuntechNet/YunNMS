from abc import ABC, abstractstaticmethod


class SNMPv3PollingAbc(ABC):
    @abstractstaticmethod
    def polling(snmp_conn: "SNMPv3Connection"):
        pass
