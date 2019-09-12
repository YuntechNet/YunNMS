from yunnms.device.entity import Interface


def test_polling(unix_snmp):
    assert len(Interface.polling(snmp_conn=unix_snmp)) != 0
