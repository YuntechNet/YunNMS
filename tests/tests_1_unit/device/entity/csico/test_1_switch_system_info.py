from yunnms.device.entity import CiscoSwitchSystemInfo


def test_str():
    csi = CiscoSwitchSystemInfo(cpu_5min=0, cpu_1min=0, cpu_5sec=5, memory_free=10, memory_used=10)
    assert str(csi) == "CiscoSwitchSystemInfo<CPU_USE: {}, MEM_USE: {}>".format(0.05, 0.5)
