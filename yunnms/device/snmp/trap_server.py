from pysnmp.entity import config
from pysnmp.hlapi.asyncore import SnmpEngine
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
from pysnmp.smi import rfc1902, compiler, view

from atomic_p2p.utils.manager import ThreadManager


class TrapServer(ThreadManager):
    def __init__(self):
        super(TrapServer, self).__init__()
        self._pdu_count = 1
        self._snmpEngine = SnmpEngine()

        self._mib_builder = self._snmpEngine.getMibBuilder()
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
            self._snmpEngine,
            udp.domainName,
            udp.UdpTransport().openServerMode(("0.0.0.0", 162)),
        )
        ntfrcv.NotificationReceiver(self._snmpEngine, self.cbFun)

    def run(self):
        self._snmpEngine.transportDispatcher.jobStarted(1)
        self._snmpEngine.transportDispatcher.runDispatcher()

    def stop(self):
        self._snmpEngine.transportDispatcher.jobFinished(1)

    def addUser(self, authentication):
        config.addV3User(
            snmpEngine=self._snmpEngine,
            userName=authentication["userName"],
            authProtocol=authentication["auth_protocol"],
            authKey=authentication["auth_key"],
            privProtocol=authentication["priv_protocol"],
            privKey=authentication["priv_key"],
            securityEngineId=v2c.OctetString(hexValue=authentication["engineId"]),
        )

    def cbFun(self, stateReference, contextEngineId, contextName, varBinds, cbCtx):
        print(
            "####################### NEW Notification(PDU_COUNT: {}) ######"
            "#################".format(self._pdu_count)
        )
        execContext = self._snmpEngine.observer.getExecutionContext(
            "rfc3412.receiveMessage:request"
        )
        print(
            "#Notification from "
            + ("@".join([str(x) for x in execContext["transportAddress"]]))
        )
        print("#ContextEngineId: {}".format(contextEngineId.prettyPrint()))
        print("#ContextName: {}".format(contextName.prettyPrint()))
        print("#SNMPVER {}".format(execContext["securityModel"]))
        print("#SecurityName {}".format(execContext["securityName"]))
        for name, val in varBinds:
            obj = rfc1902.ObjectType(rfc1902.ObjectIdentity(name), val).resolveWithMib(
                self._mib_view_controller
            )
            # print(name.prettyPrint(), val.prettyPrint())
            print(obj.prettyPrint())
        self._pdu_count += 1
