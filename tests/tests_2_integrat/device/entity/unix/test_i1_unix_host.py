from yunnms.device.entity.unix import UnixHost


def test_new(unix_snmp):
    uh = UnixHost.new(ip="127.0.0.1", snmp_conn=unix_snmp)
    assert uh.ip == "127.0.0.1"
    assert uh.system_info is not None
    assert uh.interfaces != []


def snmp_poll(unix_host):
    unix_host.snmp_poll(snmp_conn=unix_host.snmp_conn)
    assert unix_host.system_info is not None
    assert unix_host.interfaces != []
