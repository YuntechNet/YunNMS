from pytest import fixture

from pysnmp.entity import config
from pysnmp.hlapi import SnmpEngine

from yunnms.device.connection import SNMPv3Connection


@fixture
def linux_snmp():
    v3 = SNMPv3Connection(snmpEngine=SnmpEngine(), host=("127.0.0.1", 161))
    v3.authentication_register(authentication={
        "user_name": "TestLinux",
        "auth_protocol": config.usmHMACSHAAuthProtocol,
        "priv_protocol": config.usmDESPrivProtocol,
        "auth_key": "TestAuth",
        "priv_key": "TestAuth",
    })
    return v3