from yunnms.device.entity import SystemInfo


def test_polling(linux_snmp):
    assert SystemInfo.polling(snmp_conn=linux_snmp) is not None
