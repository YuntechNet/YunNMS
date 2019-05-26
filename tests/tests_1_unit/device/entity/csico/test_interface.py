from yunnms.device.entity import Interface


def test_init():
    i = Interface(name='test_interface')
    assert i.name == 'test_interface'
    assert str(i) == 'Interface<snmp_index={}, name={}, status={}>'.format(
        i.snmp_index, i.name, i.status)
