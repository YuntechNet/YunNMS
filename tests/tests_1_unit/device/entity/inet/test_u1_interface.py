from yunnms.device.entity import Interface


def test_is_trap_match(interface):
    ifIndex = "IF-MIB::ifIndex.{}".format(interface.snmp_index)
    assert interface.is_trap_match(context=None, result={
        "SNMPv2-MIB::snmpTrapOID.0": "IF-MIB::linkUp",
        ifIndex: interface.snmp_index,
    }) is True
    assert interface.is_trap_match(context=None, result={
        "SNMPv2-MIB::snmpTrapOID.0": "IF-MIB::linkDown",
        ifIndex: interface.snmp_index,
    }) is True
    assert interface.is_trap_match(context=None, result={
        "SNMPv2-MIB::snmpTrapOID.0": "IF-MIB::linkUp",
    }) is False
    assert interface.is_trap_match(context=None, result={
        "SNMPv2-MIB::snmpTrapOID.0": "OTHER-MIB::otherThing",
    }) is False


def test_trap_update(interface):
    interface.trap_update(context=None, result={
        "SNMPv2-MIB::snmpTrapOID.0": "IF-MIB::linkUp",
    })
    assert interface.status == "Up"
    interface.trap_update(context=None, result={
        "SNMPv2-MIB::snmpTrapOID.0": "IF-MIB::linkDown",
    })
    assert interface.status == "Down"


def test_str(interface):
    assert str(interface) == "Interface<NAME={}, STA: {}, PH_ADDR={}>".format(
        interface.name, interface.status, interface.phisical_address)


def test_repr(interface):
    assert repr(interface) == str(interface)
