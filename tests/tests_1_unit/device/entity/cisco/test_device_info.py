from yunnms.device.entity import DeviceInfo


def test_init(test_cisco_device_info):
    assert test_cisco_device_info.model == 'test_model'
    assert test_cisco_device_info.version == 'test_version'
    assert test_cisco_device_info.hostname == 'test_hostname'


def test_str(test_cisco_device_info):
    assert str(test_cisco_device_info) == \
        'DeviceInfo<model={}, hostname={}>'.format(
            'test_model', 'test_hostname')
