from pysnmp.entity import config
from pysnmp.hlapi.asyncore import *


class SNMPv3Connection(object):
    def __init__(self, snmpEngine, authentication):
        userName = authentication["account"]
        host = authentication["host"]
        assert type(host) == tuple
        authProtocol = self.get_protocol(
            auth_or_priv="AUTH", protocol_str=authentication["auth_protocol"]
        )
        privProtocol = self.get_protocol(
            auth_or_priv="PRIV", protocol_str=authentication["priv_protocol"]
        )
        authKey = authentication["auth_password"]
        privKey = authentication["priv_password"]
        self._snmpEngine = snmpEngine
        self._userData = UsmUserData(
            userName=userName,
            authKey=authKey,
            authProtocol=authProtocol,
            privKey=privKey,
            privProtocol=privProtocol,
        )
        self._udpTransportTarget = UdpTransportTarget(host)
        self._output = []

    def get_protocol(self, auth_or_priv, protocol_str):
        auth_or_priv = auth_or_priv.upper()
        protocol_str = protocol_str.upper() if protocol_str else None
        auth_protocols = {
            "MD5": config.usmHMACMD5AuthProtocol,
            "SHA": config.usmHMACSHAAuthProtocol,
            "SHA224": config.usmHMAC128SHA224AuthProtocol,
            "SHA256": config.usmHMAC192SHA256AuthProtocol,
            "SHA384": config.usmHMAC256SHA384AuthProtocol,
            "SHA512": config.usmHMAC384SHA512AuthProtocol,
        }
        priv_protocols = {
            "DES": config.usmDESPrivProtocol,
            "3DES": config.usm3DESEDEPrivProtocol,
            "AES": config.usmAesCfb128Protocol,
        }
        if auth_or_priv == "AUTH":
            return (
                auth_protocols[protocol_str]
                if protocol_str in auth_protocols
                else config.usmNoAuthProtocol
            )
        else:
            return (
                priv_protocols[protocol_str]
                if protocol_str in priv_protocols
                else config.usmNoPrivProtocol
            )

    def response(
        self,
        snmpEngin,
        sendRequestHandler,
        errorIndication,
        errorStatus,
        errorIndex,
        varBindTable,
        cbCtx,
    ):
        if errorIndication:
            self._output.append(errorIndication)
            return
        elif errorStatus:
            self._output.append(
                "{} = {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex) - 1][0] or "?",
                )
            )
        else:
            for varBindRow in varBindTable:
                if type(varBindRow) != list:
                    varBindRow = [varBindRow]
                for varBind in varBindRow:
                    self._output.append(" = ".join([x.prettyPrint() for x in varBind]))

    def get(self, oid):
        if type(oid) != list:
            oid = [oid]
        self._output.clear()
        for each in oid:
            assert type(each) == ObjectType
            getCmd(
                self._snmpEngine,
                self._userData,
                self._udpTransportTarget,
                ContextData(),
                each,
                cbFun=self.response,
            )
        self._snmpEngine.transportDispatcher.runDispatcher()

    def bulk(self, oid_with_NR):
        if type(oid_with_NR) != list:
            oid_with_NR = [oid_with_NR]
        self._output.clear()
        for each in oid_with_NR:
            oid = each[0]
            NR = each[1]
            assert type(oid) == ObjectType
            assert type(NR) == tuple
            bulkCmd(
                self._snmpEngine,
                self._userData,
                self._udpTransportTarget,
                ContextData(),
                NR[0],
                NR[1],
                oid,
                cbFun=self.response,
            )
        self._snmpEngine.transportDispatcher.runDispatcher()

    def output(self):
        return self._output

    def get_output(self, oid):
        self.get(oid=oid)
        return self._output

    def bulk_output(self, oid_with_NR):
        self.bulk(oid_with_NR=oid_with_NR)
        return self._output
