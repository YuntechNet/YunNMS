from typing import Tuple
from abc import ABC, abstractmethod

from pysnmp.entity import config


class SNMPConnectionABC(ABC):
    @staticmethod
    def auth_protocol_parse(auth_str: str) -> Tuple:
        return {
            "NONE": config.usmNoAuthProtocol,
            "MD5": config.usmHMACMD5AuthProtocol,
            "SHA": config.usmHMACSHAAuthProtocol,
            "SHA224": config.usmHMAC128SHA224AuthProtocol,
            "SHA256": config.usmHMAC192SHA256AuthProtocol,
            "SHA384": config.usmHMAC256SHA384AuthProtocol,
            "SHA512": config.usmHMAC384SHA512AuthProtocol,
        }[str(auth_str).upper()]

    @staticmethod
    def priv_protocol_parse(priv_str: str) -> Tuple:
        return {
            "NONE": config.usmNoPrivProtocol,
            "DES": config.usmDESPrivProtocol,
            "3DES": config.usm3DESEDEPrivProtocol,
            "AES": config.usmAesCfb128Protocol,
        }[str(priv_str).upper()]

    @abstractmethod
    def authentication_register(self, snmp_engine: "SnmpEngine", **kwargs) -> None:
        pass
