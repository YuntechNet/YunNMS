from pytest import fixture

from pysnmp.hlapi import SnmpEngine

from yunnms.device.connection import SNMPv3Connection


@fixture
def linux_snmp():
    v3 = SNMPv3Connection(snmpEngine=SnmpEngine(), host=("127.0.0.1", 161))
    v3.authentication_register(user_name="TestLinux", auth_protocol="SHA", priv_protocol="DES", auth_key="TestAuth", priv_key="TestAuth")
    return v3