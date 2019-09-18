from yunnms.device.entity import Interface


def test_snmp_polling(unix_snmp):
    assert len(Interface.snmp_polling(snmp_conn=unix_snmp)) != 0
