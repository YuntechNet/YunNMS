from .switch_device_info import SwitchDeviceInfo
from yunnms.device.entity.device import Device


class SwitchDevice(Device):

    def __init__(self, name: str, snmp_conn: 'SNMPv3Connection',
                 ssh_conn: 'SSHConnection' = None,
                 telnet_conn: 'TelnetConnection' = None) -> None:
        super(SwitchDevice, self).__init__(
            name=name, snmp_conn=snmp_conn, ssh_conn=ssh_conn,
            telnet_conn=telnet_conn)
        self._info = SwitchDeviceInfo()
        self._interfaces = []

    def update(self) -> None:
        self.__update_from_snmp_v3()

    def __update_from_snmp_v3(self) -> None:
        try:
            self._info.update_from_snmp_v3(conn=self._snmp_conn)
            self._interfaces = self._update_interfaces_from_snmp()
        except Exception:
            self.__update_from_ssh(conn=self._ssh_conn)

    def __update_from_ssh(self) -> None:
        try:
            self._info.update_from_ssh(conn=self._ssh_conn)
            self._interfaces = self._update_interfaces_from_ssh()
        except Exception as e:
            raise e

    def __update_from_telnet(self) -> None:
        pass

    def _update_interfaces_from_snmp(self) -> None:
        interfaces = []
        outputs = self._snmp_conn.get_output(oid=[
                         ObjectType(ObjectIdentity('IF-MIB', 'ifNumber', 0))])
        inter_count = int(outputs[0][outputs[0].rindex(' ') + 1:])
        outputs = self._snmp_conn.bulk_output(oid_with_NR=[
          (ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')), (0, inter_count))])
        for each in outputs[:-1]:
            snmp_index = each[each.index('ifDescr.') + 8:each.rindex(' = ')]
            name = each[each.rindex(' ') + 1:]

            output = self._snmp_conn.get_output(oid=[
             ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', snmp_index))])
            status = output[0][output[0].rindex(' ') + 1:]
            interfaces.append(Interface(snmp_index=snmp_index, name=name,
                                        status=status))
        return interfaces

    def _update_interfaces_from_ssh(self) -> None:
        self._ssh_conn.login()
        output = self._ssh_conn.send_commands(
                       commands=['show interface status'], short=False)
        self._ssh_conn.logout()

        interfaces = []
        for each in output.split('\n'):
            if 'connected' in each or 'notconnect' in each:
                interfaces.append(Interface.fromReString(re_str=each))
        return interfaces

    def __str__(self):
        return 'Device<type=CiscoSwitch>'
