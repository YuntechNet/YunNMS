from .switch_device import SwitchDevice as CiscoSwitchDevice
from .switch_device_info import SwitchDeviceInfo as CiscoSwitchDeviceInfo
from .interface import Interface

__all__ = [CiscoSwitchDevice, CiscoSwitchDeviceInfo, Interface]
