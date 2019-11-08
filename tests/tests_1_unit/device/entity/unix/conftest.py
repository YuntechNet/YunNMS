from pytest import fixture

from yunnms.device.entity.unix import UnixHost


@fixture(scope="function")
def linux_host():
    return UnixHost(ip="127.0.0.1", system_info=None, interfaces=[])
