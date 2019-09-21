from pytest import fixture

from yunnms.device.entity import Interface


@fixture
def interfaces(unix_snmp):
    return Interface.new(snmp_conn=unix_snmp)
