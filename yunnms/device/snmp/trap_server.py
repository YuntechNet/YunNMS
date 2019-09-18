from typing import Tuple
from logging import getLogger

from pysnmp.entity import config
from pysnmp.hlapi.asyncore import SnmpEngine
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
from pysnmp.smi import rfc1902, compiler, view

from atomic_p2p.utils.manager import ThreadManager


class TrapServer(ThreadManager):
    def __init__(self, host: Tuple[str, int] = ("0.0.0.0", 162), logger=getLogger()):
        super(TrapServer, self).__init__(logger=logger)
        self._host = host
        self._pdu_count = 1
        self._snmp_engine = SnmpEngine()

        self._mib_builder = self._snmp_engine.getMibBuilder()
        compiler.addMibCompiler(
            mibBuilder=self._mib_builder,
            sources=["http://mibs.snmplabs.com/asn1/@mib@"],
        )
        self._mib_builder.loadModules(
            "SNMPv2-MIB",
            "SNMP-COMMUNITY-MIB",
            "CISCO-MIB",
            "CISCO-SYSLOG-MIB",
            "CISCO-CONFIG-MAN-MIB",
            "CISCO-VTP-MIB",
        )
        self._mib_view_controller = view.MibViewController(self._mib_builder)
        config.addTransport(
            self._snmp_engine,
            udp.domainName,
            udp.UdpTransport().openServerMode(host),
        )
        ntfrcv.NotificationReceiver(self._snmp_engine, self.cbFun)

    def run(self):
        self._snmp_engine.transportDispatcher.jobStarted(1)
        self._snmp_engine.transportDispatcher.runDispatcher()

    def stop(self):
        self._snmp_engine.transportDispatcher.jobFinished(1)

    def addUser(self, authentication):
        config.addV3User(
            snmpEngine=self._snmp_engine,
            userName=authentication["userName"],
            authProtocol=authentication["auth_protocol"],
            authKey=authentication["auth_key"],
            privProtocol=authentication["priv_protocol"],
            privKey=authentication["priv_key"],
            securityEngineId=v2c.OctetString(hexValue=authentication["engineId"]),
        )

    def cbFun(self, stateReference, contextEngineId, contextName, varBinds, cbCtx):
        self.logger.info(
            "####################### NEW Notification(PDU_COUNT: {}) ######"
            "#################".format(self._pdu_count)
        )
        execContext = self._snmp_engine.observer.getExecutionContext(
            "rfc3412.receiveMessage:request"
        )
        self.logger.info(
            "#Notification from "
            + ("@".join([str(x) for x in execContext["transportAddress"]]))
        )
        self.logger.info("#ContextEngineId: {}".format(contextEngineId.prettyPrint()))
        self.logger.info("#ContextName: {}".format(contextName.prettyPrint()))
        self.logger.info("#SNMPVER {}".format(execContext["securityModel"]))
        self.logger.info("#SecurityName {}".format(execContext["securityName"]))
        for name, val in varBinds:
            obj = rfc1902.ObjectType(rfc1902.ObjectIdentity(name), val).resolveWithMib(
                self._mib_view_controller
            )
            self.logger.info(obj.prettyPrint())
        self._pdu_count += 1
