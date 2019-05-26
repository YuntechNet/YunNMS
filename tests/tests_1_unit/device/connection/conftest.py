import pytest
from yunnms.device.entity import Interface, DeviceInfo
from yunnms.device.connection import SSHConnection, TelnetConnection


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
def telnet():
    host = ('127.0.0.1', 7023)
    account = 'root'
    passwd = 'toor'
    authentication = {
        'host': host,
        'account': account,
        'password': passwd
    }
    return TelnetConnection(authentication=authentication)
