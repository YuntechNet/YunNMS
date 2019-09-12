from yunnms.device.entity.unix import UnixHost


def test_polling(unix_snmp):
    assert UnixHost.polling(ip="127.0.0.1", snmp_conn=unix_snmp) is not None
