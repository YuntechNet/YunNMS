from yunnms.device.entity import Interface


def test_polling(linux_snmp):
    assert len(Interface.polling(snmp_conn=linux_snmp)) != 0
