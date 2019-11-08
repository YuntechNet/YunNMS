from typing import List, Dict, Union
from logging import getLogger

from ....utils.abc import Serializable
from ...abc.snmp import SNMPPollABC, SNMPTrapABC


class Interface(Serializable, SNMPPollABC, SNMPTrapABC):
    @staticmethod
    def serialize(obj: "Interface", *args, **kwargs) -> Dict:
        return {
            "name": obj.name,
            "int_type": obj.int_type,
            "mtu": obj.mtu,
            "speed": obj.speed,
            "status": obj.status,
            "description": obj.description,
            "phisical_address": obj.phisical_address,
            "snmp_index": obj.snmp_index,
        }

    @staticmethod
    def deserialize(data: Dict, *args, **kwargs) -> "Interface":
        return Interface(
            name=data["name"],
            int_type=data["int_type"],
            mtu=data["mtu"],
            speed=data["speed"],
            status=data["status"],
            description=data["description"],
            phisical_address=data["phisical_address"],
            snmp_index=data["snmp_index"],
        )

    @staticmethod
    def snmp_polls(snmp_conn: "SNMPConnectionABC") -> List[Dict]:
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
    def new_interfaces(snmp_conn: "SNMPConnectionABC") -> List["Interface"]:
        interfaces = []
        prekey = "IF-MIB::"
        for each in Interface.snmp_polls(snmp_conn=snmp_conn):
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

    @staticmethod
    def new(snmp_conn: "SNMPConnectionABC", index: int) -> "Interface":
        interface = Interface(None, None, 0, 0, None)
        interface.poll_update(snmp_conn)
        return interface

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

    def snmp_poll(self, snmp_conn: "SNMPConnectionABC") -> Union[List, Dict]:
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

        output = get_g(index=self.snmp_index)
        key = "IF-MIB::"
        return [
            output[key + "ifName." + self.snmp_index],
            output[key + "ifDescr." + self.snmp_index],
            output[key + "ifType." + self.snmp_index],
            0
            if output[key + "ifMtu." + self.snmp_index]
            == "No Such Instance currently exists at this OID"
            else int(output[key + "ifMtu." + self.snmp_index]),
            int(output[key + "ifSpeed." + self.snmp_index]),
            output[key + "ifPhysAddress." + self.snmp_index],
            output[key + "ifOperStatus." + self.snmp_index],
        ]

    def poll_update(self, snmp_conn: "SNMPConnectionABC") -> None:
        name, description, int_type, mtu, speed, phisical_address, status = self.snmp_poll(
            snmp_conn
        )
        self.name = name
        self.description = description
        self.int_type = int_type
        self.mtu = mtu
        self.speed = speed
        self.phisical_address = phisical_address
        self.status = status

    def is_trap_match(self, context: Dict, result: Dict[str, str]) -> bool:
        return (
            result["SNMPv2-MIB::snmpTrapOID.0"]
            in ["IF-MIB::linkUp", "IF-MIB::linkDown"]
            and ("IF-MIB::ifIndex.{}".format(self.snmp_index)) in result
        )

    def trap_update(self, context: Dict, result: Dict) -> None:
        if result["SNMPv2-MIB::snmpTrapOID.0"] == "IF-MIB::linkUp":
            getLogger().info("{} status to up.".format(self))
            self.status = "Up"
        elif result["SNMPv2-MIB::snmpTrapOID.0"] == "IF-MIB::linkDown":
            getLogger().info("{} status to down.".format(self))
            self.status = "Down"

    def __str__(self) -> str:
        return "Interface<NAME={}, STA: {}, PH_ADDR={}>".format(
            self.name, self.status, self.phisical_address
        )

    def __repr__(self) -> str:
        return self.__str__()
