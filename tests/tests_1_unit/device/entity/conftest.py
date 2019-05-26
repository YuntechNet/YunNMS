import pytest

from yunnms.device.entity import Device, DeviceInfo


@pytest.fixture('session')
def test_device():
    return Device(name='test_name', snmp_conn=None)


@pytest.fixture('session')
def test_device_info():
    return DeviceInfo()
