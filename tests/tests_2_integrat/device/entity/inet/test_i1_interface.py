from yunnms.device.entity import Interface


def test_new(unix_snmp):
    ints = Interface.new(snmp_conn=unix_snmp)
    assert ints != []


def test_snmp_polling(unix_snmp, interfaces):
    interfaces[0].snmp_polling(snmp_conn=unix_snmp)
    assert interfaces[0].name is not None
    assert interfaces[0].description is not None
