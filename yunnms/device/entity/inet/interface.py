from typing import List, Dict
from re import compile as re_compile

from pysnmp.hlapi import ObjectType, ObjectIdentity

from yunnms.device.abc import SNMPPollingABC


class Interface(SNMPPollingABC):
    @staticmethod
    def snmp_pollings(snmp_conn: "SNMPConnectionABC") -> List[Dict]:
        return snmp_conn.bulk_by(
            oids=[
                ("IF-MIB", "ifIndex"),
                ("IF-MIB", "ifName"),
                ("IF-MIB", "ifDescr"),
                ("IF-MIB", "ifType"),
                ("IF-MIB", "ifMtu"),
                ("IF-MIB", "ifSpeed"),
                ("IF-MIB", "ifPhysAddress"),
                ("IF-MIB", "ifOperStatus"),
            ],
            count_oid=("IF-MIB", "ifNumber", 0),
        )

    @staticmethod
    def new(snmp_conn: "SNMPConnectionABC") -> List["Interface"]:
        interfaces = []
        prekey = "IF-MIB::"
        for each in Interface.snmp_pollings(snmp_conn=snmp_conn):
            index = list(each.keys())[0].split(".")[1]
            interfaces.append(
                Interface(
                    name=each[prekey + "ifName." + index],
                    int_type=each[prekey + "ifType." + index],
                    mtu=0
                    if (prekey + "ifMtu." + index) not in each
                    else int(each[prekey + "ifMtu." + index]),
                    speed=int(each[prekey + "ifSpeed." + index]),
                    status=each[prekey + "ifOperStatus." + index],
                    description=each[prekey + "ifDescr." + index],
                    phisical_address=each[prekey + "ifPhysAddress." + index],
                    snmp_index=index,
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
        snmp_index: int = 0,
    ) -> None:
        self.name = name
        self.description = description
        self.int_type = int_type
        self.mtu = mtu
        self.speed = speed
        self.status = status
        self.phisical_address = phisical_address
        self.snmp_index = snmp_index

    def snmp_polling(self, snmp_conn: "SNMPConnectionABC") -> None:
        def get_g(index):
            output = {}
            for each in [
                ("IF-MIB", "ifName", index),
                ("IF-MIB", "ifDescr", index),
                ("IF-MIB", "ifType", index),
                ("IF-MIB", "ifMtu", index),
                ("IF-MIB", "ifSpeed", index),
                ("IF-MIB", "ifPhysAddress", index),
                ("IF-MIB", "ifOperStatus", index),
            ]:
                output.update(snmp_conn.get(oid=each))
            return output

        index = str(self.snmp_index)
        output = get_g(index=index)
        key = "IF-MIB::"
        self.name = output[key + "ifName." + index]
        self.description = output[key + "ifDescr." + index]
        self.int_type = output[key + "ifType." + index]
        self.mtu = (
            0
            if output[key + "ifMtu." + index]
            == "No Such Instance currently exists at this OID"
            else int(output[key + "ifMtu." + index])
        )
        self.speed = int(output[key + "ifSpeed." + index])
        self.phisical_address = output[key + "ifPhysAddress." + index]
        self.status = output[key + "ifOperStatus." + index]

    def __str__(self) -> str:
        return "Interface<NAME={}, STA: {}, PH_ADDR={}>".format(
            self.name, self.status, self.phisical_address
        )

    def __repr__(self) -> str:
        return self.__str__()
