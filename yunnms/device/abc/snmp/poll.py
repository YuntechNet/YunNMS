from typing import List
from abc import ABC, abstractmethod, abstractstaticmethod


class SNMPPollABC(ABC):
    @abstractmethod
    def snmp_poll(
        self, snmp_conn: "SNMPConnectionABC", *args, **kwargs
    ) -> List[object]:
        """method poll data through snmp from given snmp connection
        
        Args:
            snmp_conn: A SNMPConnection use to poll.
        """
        pass

    @abstractmethod
    def poll_update(self, snmp_conn: "SNMPConnectionABC", **kwargs) -> None:
        """method poll date through snmp from given snmp connection and update instance.

        Args:
            snmp_conn: A SNMPConnection use to poll.
        """
        pass
