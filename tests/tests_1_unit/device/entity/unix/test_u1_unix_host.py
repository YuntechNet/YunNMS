from yunnms.device.entity.unix import UnixHost


def test_str(linux_snmp):
    uh = UnixHost(ip="127.0.0.1", snmp_conn=linux_snmp, system_info=None, interfaces=[])
    assert str(uh) == "UnixHost<IP={}, INT_COUNT={}>".format(
            uh.ip, len(uh.interfaces)
        )


def test_repr(linux_snmp):
    uh = UnixHost(ip="127.0.0.1", snmp_conn=linux_snmp, system_info=None, interfaces=[])
    assert repr(uh) == str(uh)
