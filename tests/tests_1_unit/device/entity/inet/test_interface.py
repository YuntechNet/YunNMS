from yunnms.device.entity import Interface


def test_init():
    i = Interface(name="test_interface", int_type="ethernetCsmacd",
                  mtu=1000, speed=1000)
    assert i.name == 'test_interface'
    assert str(i) == "Interface<NAME={}, PH_ADDR={}>".format(i.name, i.phisical_address)
