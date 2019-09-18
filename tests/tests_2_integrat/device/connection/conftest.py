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
    snmp_engine = SnmpEngine()
    conn = SNMPv3Connection(snmpEngine=snmp_engine, host=("127.0.0.1", 161))
    conn.authentication_register(snmp_engine=snmp_engine, user_name="TestLinux", auth_protocol="SHA", priv_protocol="DES", auth_key="TestAuth", priv_key="TestAuth")
    return conn
