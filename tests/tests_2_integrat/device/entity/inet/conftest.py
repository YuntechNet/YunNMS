from pytest import fixture

from yunnms.device.entity.inet import Interface


@fixture
def interfaces(unix_snmp):
    return Interface.new_interfaces(snmp_conn=unix_snmp)
