from pytest import raises


def test_oids_not_list(snmp_v3):
    with raises(ValueError) as ve:
        snmp_v3.bulk(oids={}, count=0)
    assert str(ve.value) == "parameter oids should be list with tuple."


def test_oids_list_not_contain_tuple(snmp_v3):
    with raises(ValueError) as ve:
        snmp_v3.bulk(oids=[[]], count=0)
    assert str(ve.value) == "parameter oids should be list with tuple."
