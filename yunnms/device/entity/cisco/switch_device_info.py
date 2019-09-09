import re
from typing import Tuple

from pysnmp.hlapi.asyncore import ObjectType, ObjectIdentity

from yunnms.device.entity import DeviceInfo


class SwitchDeviceInfo(DeviceInfo):
    def __init__(
        self, model: str = None, version: str = None, hostname: str = None
    ) -> None:
        super(SwitchDeviceInfo, self).__init__()
        self.model = model
        self.version = version
        self.hostname = hostname

    def __update_from_snmp_v3(self, snmp_conn: "SNMPv3Connection") -> None:
        outputs = conn.get_output(
            oid=[
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
            ]
        )
        self.model = (
            re.compile("Software, .*? Software").search(outputs[1]).group(0)[10:-9]
        )
        self.hostname = outputs[0][outputs[0].rindex(" ") + 1 :]
        self.version = re.compile("Version .*?,").search(outputs[1]).group(0)[8:-1]

    def __update_from_ssh(self, ssh_conn: "SSHConnection") -> None:
        ssh_conn.login()
        output = ssh_conn.send_commands(
            commands=["show run"], time_sleep=2, short=False
        )
        ssh_conn.logout()

        self.model = re.compile("model .*?\n").search(string).group(0)[6:-1]
        self.version = re.search("version .*?\n", string).group(0)[8:-2]
        self.hostname = re.search("hostname .*?\n", string).group(0)[9:-2]

    def __update_from_telnet(self, telnet_conn: "TelnetConnection") -> None:
        pass

    def __str__(self):
        return "DeviceInfo<model={}, hostname={}>".format(self.model, self.hostname)
