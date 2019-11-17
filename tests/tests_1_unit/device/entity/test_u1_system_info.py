

def test_str(system_info):
    assert str(system_info) == "SystemInfo<CPU_USE: {:2.02f}%, MEM_USE: {:2.02f}%>".format(0.5, 0.6)


def test_repr(system_info):
    assert repr(system_info) == str(system_info)
