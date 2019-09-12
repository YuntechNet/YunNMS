from yunnms.device.entity import SystemInfo


def test_str():
    si = SystemInfo(cpu_usage=0.5, memory_usage=0.6)
    assert str(si) == "SystemInfo<CPU_USE: {}, MEM_USE: {}>".format(0.5, 0.6)


def test_repr():
    si = SystemInfo(cpu_usage=0.5, memory_usage=0.6)
    assert repr(si) == str(si)
