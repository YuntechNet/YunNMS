import pytest

from pysnmp.entity import config
from pysnmp.hlapi import SnmpEngine

from yunnms.device.connection import SSHConnection, TelnetConnection, SNMPv3Connection


@pytest.fixture(scope='session')
def ssh():
    host = ('127.0.0.1', 7022)
    account = 'root'
    passwd = 'toor'
    authentication = {
        'host': host,
        'account': account,
        'password': passwd
    }
    return SSHConnection(authentication=authentication)


@pytest.fixture(scope='session')
def telnet(request):
    host = ('127.0.0.1', '7023')
    account = 'root'
    passwd = 'toor'
    authentication = {
        'host': host,
        'account': account,
        'password': passwd
    }
    return TelnetConnection(authentication=authentication)


@pytest.fixture(scope='module')
def snmp_v3():
    conn = SNMPv3Connection(snmpEngine=SnmpEngine(), host=("127.0.0.1", 161))
    conn.authentication_register(authentication={
        "user_name": "TestLinux",
        "auth_protocol": config.usmHMACSHAAuthProtocol,
        "priv_protocol": config.usmDESPrivProtocol,
        "auth_key": "TestAuth",
        "priv_key": "TestAuth",
    })
    return conn
