from typing import Tuple, Dict, List, Generator

from pysnmp.entity import config
from pysnmp.hlapi import (
    SnmpEngine,
    UsmUserData,
    usmHMACSHAAuthProtocol,
    usmNoPrivProtocol,
    UdpTransportTarget,
    ContextData,
    setCmd,
    getCmd,
    nextCmd,
    bulkCmd,
    ObjectType,
    ObjectIdentity,
)
from pysnmp.smi import rfc1902, compiler, view

from yunnms.device.abc import SNMPConnectionABC


class SNMPv3Connection(SNMPConnectionABC):
    @property
    def host(self):
        return self._host

    def __init__(self, snmpEngine: "SnmpEngine", host: Tuple[str, int]) -> None:
        self._snmpEngine = snmpEngine
        self._host = host
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
            "CISCO-STACK-MIB",
            "CISCO-CONFIG-MAN-MIB",
            "CISCO-VTP-MIB",
            "CISCO-PORT-SECURITY-MIB",
            "CISCO-DHCP-SNOOPING-MIB",
            "CISCO-CABLE-DIAG-MIB",
            "CISCO-L2L3-INTERFACE-CONFIG-MIB",
            "CISCO-PRIVATE-VLAN-MIB",
            "CISCO-IPSEC-FLOW-MONITOR-MIB",
            "CISCO-PORT-QOS-MIB",
        )
        self._mib_view_controller = view.MibViewController(self._mib_builder)

        self._udpTransportTarget = UdpTransportTarget(self._host)
        self._output = []

    def authentication_register(self, authentication: Dict) -> None:
        self._user = UsmUserData(
            userName=authentication["user_name"],
            authKey=authentication["auth_key"],
            privKey=authentication["priv_key"],
            authProtocol=authentication["auth_protocol"],
            privProtocol=authentication["priv_protocol"],
        )

    def __oid_init(self, oids: Tuple) -> List["ObjectType"]:
        """Build array from list of tuple which contains ObjectIdentity parameter to list of ObjectType
        
        Args:
            oids: A list contains tuple with human-readable MIB str or int.
                  Ex. ("IF-MIB", "ifNumber", 0)

        Returns:
            A list contains ObjectType.
        """
        return [ObjectType(ObjectIdentity(*each)) for each in oids]

    def __handle_result(self, query: Generator, count: int = 1) -> List[Dict[str, str]]:
        """Handle of result in queries.
        Postprocess the return value of queries with MIB resolve into human readable.

        Args:
            query: Generator from getCmd, nextCmd, or bulkCmd.
            count: int represents how many queries.

        Returns:
            A list contains dict with each query's key & value.
        
        Raises:
            RuntimeError: When SNMP query result encounter with error.
        """
        result = []
        while count != 0:
            try:
                error_indication, error_status, error_index, var_binds = next(query)
                if error_indication is None and error_status == 0:
                    items = {}
                    for (key, val) in var_binds:
                        obj = (
                            rfc1902.ObjectType(rfc1902.ObjectIdentity(key), val)
                            .resolveWithMib(self._mib_view_controller)
                            .prettyPrint()
                            .split(" = ")
                        )
                        items[obj[0]] = obj[1]
                    result.append(items)
                else:
                    raise RuntimeError(
                        "Got SNMP error: {0} {1}".format(error_indication, error_status)
                    )
            except StopIteration:
                break
            count -= 1
        return result

    def set(self, oid: Tuple, **options) -> Dict:
        if type(oid) is not tuple:
            raise ValueError("parameter oid should be tuple.")
        query = setCmd(
            self._snmpEngine,
            self._user,
            self._udpTransportTarget,
            ContextData(),
            ObjectType(ObjectIdentity(*oid[0]), oid[1]),
            **options
        )
        return self.__handle_result(query=query, count=1)[0]

    def get(self, oid: Tuple, **options) -> Dict:
        """GET snmp query

        Args:
            oid: Tuple with human-readable MIB str or int.
                 Ex. ("IF-MIB", "ifNumber", 0)
        
        Returns:
            Query result with given oid.

        Raises:
            ValueError: when oid is not a tuple.
        """
        if type(oid) is not tuple:
            raise ValueError("parameter oid should be tuple.")
        query = getCmd(
            self._snmpEngine,
            self._user,
            self._udpTransportTarget,
            ContextData(),
            *self.__oid_init(oids=[oid]),
            **options
        )
        return self.__handle_result(query=query)[0]

    def next(
        self, oids: List[Tuple], lexicographicMode: bool = False, **options
    ) -> Dict:
        """NEXT snmp query

        Args:
            oids: List contains tuples with human-readable MIB str or int.
                  Ex. [('IF-MIB', 'ifName'), ('IF-MIB', 'ifDescr')]
            lexicographicMode: Please reference at pysnmp.hlapi.asyncore.sync.cmdgen#nextCmd
        
        Returns:
            Query result with given oid.

        Raises:
            ValueError: when oids is not a list contains tuple.
        """
        if type(oids) is not list:
            raise ValueError("parameter oids should be list with tuple.")
        for each in oids:
            if type(each) is not tuple:
                raise ValueError("parameter oids should be list with tuple.")

        query = nextCmd(
            self._snmpEngine,
            self._user,
            self._udpTransportTarget,
            ContextData(),
            *self.__oid_init(oids=oids),
            lexicographicMode=lexicographicMode,
            **options
        )

        result = self.__handle_result(query=query, count=len(oids))
        return result[0] if len(result) > 0 else result

    def bulk(
        self, oids: List[Tuple], count: int, start_from: int = 0, **options
    ) -> List[Dict]:
        """BULK snmp query

        Args:
            oids: List contains tuples with human-readable MIB str or int.
                  Ex. [('IF-MIB', 'ifName'), ('IF-MIB', 'ifDescr')]
            count: length to be read.
            start_from: start index to be query.
        
        Returns:
            Each result in dict with query key & its value and put in list.
        
        Raises:
            ValueError: when oids is not a list contains tuple.
        """
        if type(oids) is not list:
            raise ValueError("parameter oids should be list with tuple.")
        for each in oids:
            if type(each) is not tuple:
                raise ValueError("parameter oids should be list with tuple.")

        query = bulkCmd(
            self._snmpEngine,
            self._user,
            self._udpTransportTarget,
            ContextData(),
            start_from,
            count,
            *self.__oid_init(oids=oids),
            **options
        )
        return self.__handle_result(query=query, count=count)

    def bulk_by(
        self, oids: List[Tuple], count_oid: Tuple, start_from: int = 0, **options
    ) -> List[Dict]:
        """BULK snmp query with length which base on another oid query.
        
        Args:
            oids: List contains tuples with human-readable MIB str or int.
                  Ex. [('IF-MIB', 'ifName'), ('IF-MIB', 'ifDescr')]
            count_oid: oid in Tuple which can get a converable int string.
                  Ex. ('IF-MIB', 'ifNumber', 0)
                      This OID can get interfaces count.
            start_from: start index to be query.

        Returns:
            Each result in dict with query key & its value and put in list.

        Raises:
            ValueError:
                A. given oids is not a list contains tuple.
                B. count_oid's query returns a un-converable string.
        """
        count = int(self.get(oid=count_oid)["{0}::{1}.{2}".format(*count_oid)])
        return self.bulk(oids=oids, count=count, start_from=start_from, **options)
