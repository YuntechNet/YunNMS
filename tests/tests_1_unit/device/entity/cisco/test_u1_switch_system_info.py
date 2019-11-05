


def test_calculate(cisco_system_info):
    cpu = 60 # 60%
    memory = 70 # 70%
    free = 30
    used = 70
    cisco_system_info.cpu_5min = cpu
    cisco_system_info.memory_used = used
    cisco_system_info.memory_free = free
    assert cisco_system_info.cpu_usage != cpu
    assert cisco_system_info.memory_usage != memory
    cisco_system_info.calculate()
    assert cisco_system_info.cpu_usage == cpu
    assert cisco_system_info.memory_usage == memory


def test_str(cisco_system_info):
    assert str(cisco_system_info) == "CiscoSwitchSystemInfo<CPU_USE: {:2.02f}%, MEM_USE: {:2.02f}%>".format(
        0, 10 / (10 + 10) * 100)
