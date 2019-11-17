from pytest import fixture

from pysnmp.entity import config
from pysnmp.hlapi import SnmpEngine

from yunnms.device.connection import SNMPv3Connection
from yunnms.device.entity import SystemInfo


@fixture(scope='module')
def unix_snmp():
    conn = SNMPv3Connection(snmpEngine=SnmpEngine(), host=("127.0.0.1", 161))
    conn.authentication_register(authentication={
        "user_name": "TestLinux",
        "auth_protocol": config.usmHMACSHAAuthProtocol,
        "priv_protocol": config.usmDESPrivProtocol,
        "auth_key": "TestAuth",
        "priv_key": "TestAuth",
    })
    return conn


@fixture
def system_info(unix_snmp):
    return SystemInfo.new(snmp_conn=unix_snmp)
