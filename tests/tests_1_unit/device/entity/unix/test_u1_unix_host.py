from yunnms.device.entity.unix import UnixHost


def test_str():
    uh = UnixHost(ip="127.0.0.1", system_info=None, interfaces=[])
    assert str(uh) == "UnixHost<IP={}, INT_COUNT={}>".format(
            uh.ip, len(uh.interfaces)
        )


def test_repr():
    uh = UnixHost(ip="127.0.0.1", system_info=None, interfaces=[])
    assert repr(uh) == str(uh)
