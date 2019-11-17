from atomic_p2p.peer.command import Command

from ..entity.cisco import CiscoSwitch


class SyslogListCmd(Command):
    """
        Command to list all syslog in Switch.
        Usage in prompt:
            device syslogs [name]
    """

    def __init__(self, device_manager):
        super().__init__("syslogs")
        self.device_manager = device_manager
        self.peer = device_manager.peer

    def _execute(self, msg_arr):
        device = self.device_manager.get_device(name=msg_arr[0])
        if device is None:
            return "There is no device match that name."
        elif isinstance(device, CiscoSwitch) is False:
            return "Device with given name is not a Cisco device."
        else:
            output_text = "Syslog:\n"
            for each in device.syslog.logs:
                output_text += " - {}\n".format(each)
            output_text += "[---End of list---]"
            return output_text
