from .switch_device import SwitchDevice as CiscoSwitchDevice
from .switch_device_info import SwitchDeviceInfo as CiscoSwitchDeviceInfo
from .switch_system_info import CiscoSwitchSystemInfo

__all__ = [
    "CiscoSwitchSystemInfo",
    "CiscoSwitchDevice",
    "CiscoSwitchDeviceInfo"
]
