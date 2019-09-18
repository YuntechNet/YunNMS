from yunnms.device.entity import SystemInfo


def test_snmp_polling(unix_snmp):
    assert SystemInfo.snmp_polling(snmp_conn=unix_snmp) is not None
