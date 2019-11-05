from pytest import fixture

from yunnms.device.entity import SystemInfo


@fixture(scope="function")
def system_info():
    return SystemInfo(name="name", description="description", cpu_usage=0.5, memory_usage=0.6)
    