from typing import List
from abc import ABC, abstractmethod


class DeviceABC(ABC):
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
    def update(self) -> None:
        pass

    def __str__(self) -> str:
        return "{}<IP={}, INT_COUNT={}>".format(
            type(self).__name__, self.ip, len(self.interfaces)
        )

    def __repr__(self) -> str:
        return self.__str__()
