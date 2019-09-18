from yunnms.device.entity.unix import UnixHost


def test_snmp_polling(unix_snmp):
    assert UnixHost.snmp_polling(ip="127.0.0.1", snmp_conn=unix_snmp) is not None
