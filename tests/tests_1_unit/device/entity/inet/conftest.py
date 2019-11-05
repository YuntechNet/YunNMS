from pytest import fixture

from yunnms.device.entity import Interface


@fixture(scope="function")
def interface():
    return Interface(name="test_interface", int_type="ethernetCsmacd",
                     mtu=1000, speed=1000, status="up")