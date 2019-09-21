from yunnms.device.entity.cisco import CiscoSwitchSystemInfo


def test_str():
    csi = CiscoSwitchSystemInfo(name="name", description="description", cpu_5min=0, cpu_1min=0, cpu_5sec=5, memory_free=10, memory_used=10)
    assert str(csi) == "CiscoSwitchSystemInfo<CPU_USE: {:2.02f}%, MEM_USE: {:2.02f}%>".format(0, 10 / (10 + 10) * 100)
