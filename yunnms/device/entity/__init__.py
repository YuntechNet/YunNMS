from .device import Device
from .device_info import DeviceInfo
from .cisco import CiscoSwitchDevice, CiscoSwitchDeviceInfo, Interface
from .enums import SpeedRate

__all__ = [
    "Device",
    "DeviceInfo",
    "SpeedRate",
    "Interface",
    "CiscoSwitchDevice",
    "CiscoSwitchDeviceInfo",
]
