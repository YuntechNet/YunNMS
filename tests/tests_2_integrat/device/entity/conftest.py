from pytest import fixture

from pysnmp.hlapi import SnmpEngine

from yunnms.device.connection import SNMPv3Connection


@fixture(scope='module')
def linux_snmp():
    return SNMPv3Connection(snmpEngine=SnmpEngine(), authentication={
        "account": "TestLinux",
        "host": ("127.0.0.1", 161),
        "auth_protocol": "SHA",
        "auth_password": "TestAuth",
        "priv_protocol": "DES",
        "priv_password": "TestAuth",
    })
