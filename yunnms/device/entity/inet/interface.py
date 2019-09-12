from re import compile as re_compile
from pysnmp.hlapi import ObjectType, ObjectIdentity

from yunnms.device.abc import SNMPv3PollingAbc


class Interface(SNMPv3PollingAbc):
    @staticmethod
    def polling(snmp_conn: "SNMPv3Connection") -> "Interface":
        interfaces = []
        prekey = "IF-MIB::"
        for each in snmp_conn.bulk_by(
            oids=[
                ("IF-MIB", "ifName"),
                ("IF-MIB", "ifDescr"),
                ("IF-MIB", "ifType"),
                ("IF-MIB", "ifMtu"),
                ("IF-MIB", "ifSpeed"),
                ("IF-MIB", "ifPhysAddress"),
                ("IF-MIB", "ifAdminStatus"),
            ],
            count_oid=("IF-MIB", "ifNumber", 0),
        ):
            index = list(each.keys())[0].split(".")[1]
            interfaces.append(
                Interface(
                    name=each[prekey + "ifName." + index],
                    int_type=each[prekey + "ifType." + index],
                    mtu=int(each[prekey + "ifMtu." + index]),
                    speed=int(each[prekey + "ifSpeed." + index]),
                    status=each[prekey + "ifAdminStatus." + index],
                    description=each[prekey + "ifDescr." + index],
                    phisical_address=each[prekey + "ifPhysAddress." + index],
                )
            )
        return interfaces

    def __init__(
        self,
        name: str,
        int_type: str,
        mtu: int,
        speed: int,
        status: str,
        description: str = "",
        phisical_address: str = "",
    ) -> None:
        self.name = name
        self.description = description
        self.int_type = int_type
        self.mtu = mtu
        self.speed = speed
        self.status = status
        self.phisical_address = phisical_address

    def __str__(self) -> str:
        return "Interface<NAME={}, STA: {}, PH_ADDR={}>".format(self.name, self.status, self.phisical_address)

    def __repr__(self) -> str:
        return self.__str__()
