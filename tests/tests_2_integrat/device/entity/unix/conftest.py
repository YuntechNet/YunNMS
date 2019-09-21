from pytest import fixture

from yunnms.device.entity.unix import UnixHost


@fixture
def unix_host(unix_snmp):
    return UnixHost.new(ip="127.0.0.1", snmp_conn=unix_snmp)
