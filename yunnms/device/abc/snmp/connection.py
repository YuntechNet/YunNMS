from typing import Tuple
from abc import ABC, abstractmethod

from pysnmp.entity import config


class SNMPConnectionABC(ABC):
    def auth_protocol_parse(self, auth_protocol: str) -> Tuple:
        return {
            "NONE": config.usmNoAuthProtocol,
            "MD5": config.usmHMACMD5AuthProtocol,
            "SHA": config.usmHMACSHAAuthProtocol,
            "SHA224": config.usmHMAC128SHA224AuthProtocol,
            "SHA256": config.usmHMAC192SHA256AuthProtocol,
            "SHA384": config.usmHMAC256SHA384AuthProtocol,
            "SHA512": config.usmHMAC384SHA512AuthProtocol,
        }[str(auth_protocol).upper()]

    def priv_protocol_parse(self, priv_protocol: str) -> Tuple:
        return {
            "NONE": config.usmNoPrivProtocol,
            "DES": config.usmDESPrivProtocol,
            "3DES": config.usm3DESEDEPrivProtocol,
            "AES": config.usmAesCfb128Protocol,
        }[str(priv_protocol).upper()]

    @abstractmethod
    def authentication_register(self, snmp_engine: "SnmpEngine", **kwargs) -> None:
        pass
