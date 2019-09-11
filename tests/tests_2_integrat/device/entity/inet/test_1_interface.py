from yunnms.device.entity import Interface


def test_polling(snmp_v3):
    assert len(Interface.polling(snmp_conn=snmp_v3)) != 0
