
def test_get(snmp_v3):
    assert snmp_v3.get(oid=('IF-MIB', 'ifNumber', 0)) is not None


def test_next(snmp_v3):
    assert snmp_v3.next(oids=[
        ('IF-MIB', 'ifName'),
        ('IF-MIB', 'ifDescr'),
        ('IF-MIB', 'ifType'),
        ('IF-MIB', 'ifMtu'),
        ('IF-MIB', 'ifSpeed'),
        ('IF-MIB', 'ifPhysAddress'),
    ]) is not None


def test_bulk(snmp_v3):
    count = int(snmp_v3.get(oid=('IF-MIB', 'ifNumber', 0))["IF-MIB::ifNumber.0"])
    assert snmp_v3.bulk(oids=[
        ('IF-MIB', 'ifName'),
        ('IF-MIB', 'ifDescr'),
        ('IF-MIB', 'ifType'),
        ('IF-MIB', 'ifMtu'),
        ('IF-MIB', 'ifSpeed'),
        ('IF-MIB', 'ifPhysAddress'),
    ], count=count) is not None


def test_bulk_by(snmp_v3):
    assert snmp_v3.bulk_by(oids=[
        ('IF-MIB', 'ifName'),
        ('IF-MIB', 'ifDescr'),
        ('IF-MIB', 'ifType'),
        ('IF-MIB', 'ifMtu'),
        ('IF-MIB', 'ifSpeed'),
        ('IF-MIB', 'ifPhysAddress'),
    ], count_oid=('IF-MIB', 'ifNumber', 0)) is not None
