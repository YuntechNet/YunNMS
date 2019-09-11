from abc import ABC, abstractstaticmethod


class SNMPv3PollingAbs(ABC):

    @abstractstaticmethod
    def polling(snmp_conn: "SNMPv3Connection"):
        pass