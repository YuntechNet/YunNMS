import pytest

from yunnms.device.entity import CiscoSwitchDevice, CiscoSwitchDeviceInfo


@pytest.fixture(scope='session')
def test_cisco_device_info():
    return CiscoSwitchDeviceInfo(
        model='test_model', version='test_version', hostname='test_hostname')


@pytest.fixture(scope='session')
def test_cisco_switch_device():
    return CiscoSwitchDevice(
        name='test')
