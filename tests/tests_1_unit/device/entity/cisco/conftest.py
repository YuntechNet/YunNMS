from pytest import fixture

from yunnms.device.entity.inet import Interface
from yunnms.device.entity.cisco import CiscoSwitchSystemInfo, CiscoSwitch


@fixture(scope="function")
def cisco_system_info():
    return CiscoSwitchSystemInfo(
        name="name",
        description="description",
        cpu_5min=0,
        cpu_1min=0,
        cpu_5sec=5,
        memory_free=10,
        memory_used=10
    )


@fixture(scope="function")
def cisco_switch():
    return CiscoSwitch(ip="127.0.0.1", snmp_conn=None, system_info=None, interfaces=[
        Interface(name="test_interface1", int_type="ethernetCsmacd", mtu=1000, speed=1000, status="up", snmp_index=1),
        Interface(name="test_interface2", int_type="ethernetCsmacd", mtu=1000, speed=1000, status="up", snmp_index=2),
    ])
