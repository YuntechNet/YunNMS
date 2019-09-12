from re import compile as re_compile
from pysnmp.hlapi import ObjectType, ObjectIdentity

from yunnms.device.abc import SNMPv3PollingAbc


class Interface(SNMPv3PollingAbc):
    @staticmethod
    def polling(snmp_conn: "SNMPv3Connection") -> "Interface":
        return [
            Interface(*each.values())
            for each in snmp_conn.bulk_by(
                oids=[
                    ("IF-MIB", "ifName"),
                    ("IF-MIB", "ifDescr"),
                    ("IF-MIB", "ifType"),
                    ("IF-MIB", "ifMtu"),
                    ("IF-MIB", "ifSpeed"),
                    ("IF-MIB", "ifPhysAddress"),
                ],
                count_oid=("IF-MIB", "ifNumber", 0),
            )
        ]

    def __init__(
        self,
        name: str,
        int_type: str,
        mtu: int,
        speed: int,
        description: str = "",
        phisical_address: str = "",
    ) -> None:
        self.name = name
        self.description = description
        self.int_type = int_type
        self.mtu = mtu
        self.speed = speed
        self.phisical_address = phisical_address

    def __str__(self) -> str:
        return "Interface<NAME={}, PH_ADDR={}>".format(self.name, self.phisical_address)

    def __repr__(self) -> str:
        return self.__str__()
