from pytest import raises


def test_oid_not_tuple(snmp_v3):
    with raises(ValueError) as ve:
        snmp_v3.get(oid=[])
    assert str(ve.value) == "parameter oid should be tuple."
