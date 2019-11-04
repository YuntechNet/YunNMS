from yunnms.device.entity import Interface


def test_new_interfaces(unix_snmp):
    ints = Interface.new_interfaces(snmp_conn=unix_snmp)
    assert ints != []


def test_snmp_poll(unix_snmp, interfaces):
    interfaces[0].snmp_poll(snmp_conn=unix_snmp)
    assert interfaces[0].name is not None
    assert interfaces[0].description is not None
