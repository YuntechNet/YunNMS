from atomic_p2p.peer.command import Command

from ..entity.cisco.switch import CiscoSwitch
from ..abc.snmp.connection import SNMPConnectionABC
from ..connection import SNMPv3Connection as SNMPv3
from .connection import ConnectionCmd
from .cisco import SyslogListCmd

__all__ = [
    "HelpCmd",
    "ListCmd",
    "NewCmd",
    "RemoveCmd",
    "ConnectionCmd",
    "SyslogListCmd",
]


class HelpCmd(Command):
    """HelpCmd
        show the help for peers.
        Usage in prompt: peer help [cmd]
    """

    def __init__(self, device_manager):
        super(HelpCmd, self).__init__("help")
        self.device_manager = device_manager
        self.peer = device_manager.peer

    def _execute(self, msg_arr):
        if msg_arr != [] and msg_arr[0] in self.peer.commands:
            return self.peer.commands[msg_arr[0]].__doc__
        else:
            return (
                "peer [cmd] <options>\n"
                " - list                                           "
                "list all services in list.\n"
                " - device add [ssh/telnet] [ip:port] [account] [passwor"
                "d]\n   device add snmp [ip:port] [account] [password] ["
                "link-level] [auth_protocol] [auth_passowrd] [priv_proto"
                "col] [priv_password]\n"
                "  add service.\n"
                " - help [cmd]                                     "
                "show help msg of sepecific command."
            )


class ListCmd(Command):
    """ListCmd
        list all services in list
        Usage in prompt: device list
    """

    def __init__(self, device_manager):
        super(ListCmd, self).__init__("list")
        self.device_manager = device_manager
        self.peer = device_manager.peer

    def _execute(self, msg_arr):
        if len(self.device_manager._devices.items()) == 0:
            return "There is no devices in manager."
        else:
            output_text = "Current device info:\n"
            for each in self.device_manager._devices.items():
                output_text += " - {}\n".format(each)
            output_text += "[---End of list---]"
            return output_text


class NewCmd(Command):
    """
        Command to new a device.
        Usage in prompt:
            device new device_type device_name ip account auth_protocol
             auth_password priv_protocol priv_password engine_id
    """

    def __init__(self, device_manager):
        super(NewCmd, self).__init__("new")
        self.device_manager = device_manager
        self.peer = device_manager.peer

    def _execute(self, msg_arr):
        device_type = msg_arr[0]
        device_name = msg_arr[1]
        if device_name in self.device_manager._devices:
            return "{} already exists".format(device_name)

        authentication = {
            "user_name": msg_arr[3],
            "auth_protocol": SNMPConnectionABC.auth_protocol_parse(
                auth_str=msg_arr[4]
            ),
            "auth_key": msg_arr[5],
            "priv_protocol": SNMPConnectionABC.priv_protocol_parse(
                priv_str=msg_arr[6]
            ),
            "priv_key": msg_arr[7],
        }
        snmpv3 = SNMPv3(
            snmpEngine=self.device_manager._snmp_engine, host=(msg_arr[2], 161)
        )
        snmpv3.authentication_register(authentication=authentication)
        if len(msg_arr) == 9:
            authentication["engine_id"] = msg_arr[8]
            self.device_manager.trap_server.add_user(authentication=authentication)
        if device_type == "CiscoSwitch":
            added_device = CiscoSwitch.new(ip=msg_arr[2], snmp_conn=snmpv3)
            self.device_manager.add_device(added_device)
            return "{} added.".format(str(added_device))
        return "Added failed with device type {}.".format(device_type)


class RemoveCmd(Command):
    """
        Command to remove a device.
    """

    def __init__(self, device_manager):
        super(RemoveCmd, self).__init__("remove")
        self.device_manager = device_manager
        self.peer = device_manager.peer

    def _execute(self, msg_arr):
        pass
