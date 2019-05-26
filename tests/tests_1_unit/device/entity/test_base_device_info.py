import pytest


def test_update(test_device_info):
    with pytest.raises(NotImplementedError):
        test_device_info.update()


def test___update_from_snmp_v3(test_device_info):
    with pytest.raises(NotImplementedError):
        test_device_info._DeviceInfo__update_from_snmp_v3(snmp_conn=None)


def test___update_from_ssh(test_device_info):
    with pytest.raises(NotImplementedError):
        test_device_info._DeviceInfo__update_from_ssh(ssh_conn=None)


def test___update_from_telnet(test_device_info):
    with pytest.raises(NotImplementedError):
        test_device_info._DeviceInfo__update_from_telnet(telnet_conn=None)
