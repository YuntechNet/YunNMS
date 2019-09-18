from pytest import fixture

from pysnmp.hlapi import SnmpEngine

from yunnms.device.connection import SNMPv3Connection


@fixture(scope='module')
def unix_snmp():
    snmp_engine = SnmpEngine()
    conn = SNMPv3Connection(snmpEngine=snmp_engine, host=("127.0.0.1", 161))
    conn.authentication_register(snmp_engine=snmp_engine, user_name="TestLinux", auth_protocol="SHA", priv_protocol="DES", auth_key="TestAuth", priv_key="TestAuth")
    return conn
