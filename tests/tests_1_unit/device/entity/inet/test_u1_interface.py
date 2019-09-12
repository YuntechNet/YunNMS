from yunnms.device.entity import Interface


def test_str():
    i = Interface(name="test_interface", int_type="ethernetCsmacd",
                  mtu=1000, speed=1000, status="up")
    assert str(i) == "Interface<NAME={}, STA: {}, PH_ADDR={}>".format(i.name, i.status, i.phisical_address)


def test_repr():
    i = Interface(name="test_interface", int_type="ethernetCsmacd",
                  mtu=1000, speed=1000, status="up")
    assert repr(i) == str(i)
