import pytest


def test_init(test_device):
    assert test_device._name == 'test_name'
    assert test_device._snmp_conn is None
    assert test_device._ssh_conn is None
    assert test_device._telnet_conn is None


def test_set_snmp_conn(test_device):
    test_device.set_snmp_conn(snmp_conn='test')
    assert test_device._snmp_conn == 'test'


def test_set_ssh_conn(test_device):
    test_device.set_ssh_conn(ssh_conn='test')
    assert test_device._ssh_conn == 'test'


def test_set_telnet_conn(test_device):
    test_device.set_telnet_conn(telnet_conn='test')
    assert test_device._telnet_conn == 'test'


def test_update(test_device):
    with pytest.raises(NotImplementedError):
        test_device.update()


def test___update_from_snmp_v3(test_device):
    with pytest.raises(NotImplementedError):
        test_device._Device__update_from_snmp_v3()


def test___update_from_ssh(test_device):
    with pytest.raises(NotImplementedError):
        test_device._Device__update_from_ssh()


def test___update_from_telnet(test_device):
    with pytest.raises(NotImplementedError):
        test_device._Device__update_from_telnet()


def test_str(test_device):
    with pytest.raises(NotImplementedError):
        str(test_device)
