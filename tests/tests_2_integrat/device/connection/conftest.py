import pytest

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
    return SNMPv3Connection(snmpEngine=SnmpEngine(), authentication={
        "account": "TestLinux",
        "host": ("127.0.0.1", 161),
        "auth_protocol": "SHA",
        "auth_password": "TestAuth",
        "priv_protocol": "DES",
        "priv_password": "TestAuth",
    })
