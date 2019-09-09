from atomic_p2p.utils.command import Command

from ..entity import Device
from ..connection import SNMPv3Connection as SNMPv3
from ..entity import CiscoSwitchDevice

from .connection import ConnectionCmd

__all__ = ["HelpCmd", "ListCmd", "NewCmd", "RemoveCmd", "ConnectionCmd"]


class HelpCmd(Command):
    """HelpCmd
        show the help for peers.
        Usage in prompt: peer help [cmd]
    """

    def __init__(self, peer):
        super(HelpCmd, self).__init__("help")
        self.peer = peer

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
        msg = ""
        hostname = msg_arr[0]
        for each in self.device_manager._devices.items():
            if each.info.hostname == hostname:
                for every in each.interfaces:
                    msg = "{}\n{}".format(msg, str(every))
        return msg


class NewCmd(Command):
    """
        Command to new a device.
        Usage in prompt:
            device new device_type device_name ip account auth_protocol
             auth_password priv_protocol priv_password
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

        snmpv3 = SNMPv3(
            snmpEngine=self.device_manager._snmp_engine,
            authentication={
                "host": (msg_arr[2], 161),
                "account": msg_arr[3],
                "authProtocol": msg_arr[4],
                "authPassword": msg_arr[5],
                "privProtocol": msg_arr[6],
                "privPassword": msg_arr[7],
            },
        )
        if device_type == "CiscoSwitch":
            added_device = CiscoSwitchDevice(name=device_name, snmp_conn=snmpv3)
            self.device_manager.add_device(device_name, added_device)
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
