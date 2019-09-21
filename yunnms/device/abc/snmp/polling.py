from abc import ABC, abstractmethod, abstractstaticmethod


class SNMPPollingABC(ABC):
    @abstractstaticmethod
    def new(snmp_conn: "SNMPConnectionABC", **kwargs) -> object:
        pass

    @abstractmethod
    def snmp_polling(self, snmp_conn: "SNMPConnectionABC") -> object:
        """method shows how to poll data through snmp
        
        Args:
            snmp_conn: A SNMPConnection use to poll.
        """
        pass
