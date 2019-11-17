from typing import List, Dict
from abc import abstractmethod

from ...utils.abc import Serializable
from ..entity import DeviceType, SystemInfo
from ..entity.inet.interface import Interface


class DeviceABC(Serializable):
    @staticmethod
    def serialize(obj: "DeviceABC", *args, **kwargs) -> Dict:
        return {
            "ip": obj.ip,
            "device_type": obj.device_type,
            "system_info": SystemInfo.serialize(obj=obj.system_info),
            "interfaces": [Interface.serialize(obj=each) for each in obj.interfaces],
        }

    @staticmethod
    def deserialize(data: Dict, *args, **kwargs) -> "DeviceABC":
        return DeviceABC(
            ip=data["ip"],
            device_type=DeviceType(data["device_type"]),
            system_info=SystemInfo.deserialize(data=data["system_info"]),
            interfaces=[
                Interface.deserialize(data=each) for each in data["interfaces"]
            ],
        )

    def __init__(
        self,
        ip: str,
        device_type: "DeviceType",
        system_info: "SystemInfo",
        interfaces: List["Interface"],
    ) -> None:
        self.ip = ip
        self.device_type = device_type
        self.system_info = system_info
        self.interfaces = interfaces

    @abstractmethod
    def update(self, data: Dict, *args, **kwargs) -> None:
        pass

    def __str__(self) -> str:
        return "{}<IP={}, INT_COUNT={}>".format(
            type(self).__name__, self.ip, len(self.interfaces)
        )

    def __repr__(self) -> str:
        return self.__str__()
