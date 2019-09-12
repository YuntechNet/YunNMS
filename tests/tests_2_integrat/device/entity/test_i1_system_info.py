from yunnms.device.entity import SystemInfo


def test_polling(unix_snmp):
    assert SystemInfo.polling(snmp_conn=unix_snmp) is not None
