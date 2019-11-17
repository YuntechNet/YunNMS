from typing import Dict

from atomic_p2p.logging import getLogger

from ...abc.snmp import SNMPTrapABC


class LogEntry(object):
    def __init__(
        self,
        index: int,
        facility: str,
        severity: str,
        msg_name: str,
        msg_text: str,
        timestamp: int,
    ):
        self.index = index
        self.facility = facility
        self.severity = severity
        self.msg_name = msg_name
        self.msg_text = msg_text
        self.timestamp = timestamp

    def __str__(self) -> str:
        return "Log<f={}, s={}, n={}, t={}, ts={}".format(
            self.facility, self.severity, self.msg_name, self.msg_text, self.timestamp
        )

    def __repr__(self) -> str:
        return self.__str__()


class Syslog(SNMPTrapABC):
    @staticmethod
    def new(snmp_conn: "SNMPConnectionABC") -> "Syslog":
        return Syslog()

    def __init__(self):
        self.logs = []

    def is_trap_match(self, context: Dict, result: Dict[str, str]) -> bool:
        return (
            "SNMPv2-MIB::snmpTrapOID.0" in result
            and result["SNMPv2-MIB::snmpTrapOID.0"]
            == "CISCO-SYSLOG-MIB::clogMessageGenerated"
        )

    def trap_update(self, context: Dict, result: Dict) -> None:
        logResult = {
            k: v for (k, v) in result.items() if "CISCO-SYSLOG-MIB::clogHist" in k
        }
        index = int(next(iter(logResult.keys())).split(".")[1])
        self.logs.append(
            LogEntry(
                index=index,
                facility=logResult[
                    "CISCO-SYSLOG-MIB::clogHistFacility.{}".format(index)
                ],
                severity=logResult[
                    "CISCO-SYSLOG-MIB::clogHistSeverity.{}".format(index)
                ],
                msg_name=logResult[
                    "CISCO-SYSLOG-MIB::clogHistMsgName.{}".format(index)
                ],
                msg_text=logResult[
                    "CISCO-SYSLOG-MIB::clogHistMsgText.{}".format(index)
                ],
                timestamp=logResult[
                    "CISCO-SYSLOG-MIB::clogHistTimestamp.{}".format(index)
                ],
            )
        )
