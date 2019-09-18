from abc import ABC, abstractstaticmethod


class SNMPPollingABC(ABC):
    @abstractstaticmethod
    def snmp_polling(snmp_conn: "SNMPConnectionABC"):
        pass
