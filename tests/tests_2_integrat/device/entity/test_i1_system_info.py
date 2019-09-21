from yunnms.device.entity import SystemInfo


def test_new(unix_snmp):
    si = SystemInfo.new(snmp_conn=unix_snmp)
    assert si.name is not None
    assert si.description is not None


def test_snmp_polling(unix_snmp, system_info):
    system_info.snmp_polling(snmp_conn=unix_snmp)
    assert system_info.name is not None
    assert system_info.description is not None
