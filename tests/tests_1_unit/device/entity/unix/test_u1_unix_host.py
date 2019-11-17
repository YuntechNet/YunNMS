

def test_is_trap_match(linux_host):
    assert linux_host.is_trap_match(context={
        "transportAddress": (linux_host.ip, 12345),
    }, result=None) is True
    assert linux_host.is_trap_match(context={
        "transportAddress": ("other_ip", 12345),
    }, result=None) is False


def test_str(linux_host):
    assert str(linux_host) == "UnixHost<IP={}, INT_COUNT={}>".format(
        linux_host.ip, len(linux_host.interfaces)
    )


def test_repr(linux_host):
    assert repr(linux_host) == str(linux_host)
