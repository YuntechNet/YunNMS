

class Device(object):
    """Base class for extend"""

    def __init__(self, name: str, snmp_conn: 'SNMPv3Connection',
                 ssh_conn: 'SSHConnection' = None,
                 telnet_conn: 'TelnetConnection' = None) -> None:
        """Init of Device

        Attribute:
            name: name of this device.
            snmp_conn: SNMPv3Connection for this device.
            ssh_conn: SSHConnection for this device.
            telnet_conn: TelnetConnection for this device.
        """
        self._name = name
        self._snmp_conn = snmp_conn
        self._ssh_conn = ssh_conn
        self._telnet_conn = telnet_conn

    def set_snmp_conn(self, snmp_conn: 'SNMPv3Connection') -> None:
        self._snmp_conn = snmp_conn

    def set_ssh_conn(self, ssh_conn: 'SSHConnection') -> None:
        self._ssh_conn = ssh_conn

    def set_telnet_conn(self, telnet_conn: 'TelnetConnection') -> None:
        self._telnet_conn = telnet_conn

    def update(self) -> None:
        """Main update method called from manager loop"""
        raise NotImplementedError

    def __update_from_snmp_v3(self) -> None:
        """Implementation of SNMPv3 update informations
        This method is only called by update method.
        And it's explains how to use SNMPv3Connection to get informations.
        """
        raise NotImplementedError

    def __update_from_ssh(self) -> None:
        """Implementation of SSH update informations
        This method is only called by update method.
        And it's explains how to use SSHConnection to get informations.
        """
        raise NotImplementedError

    def __update_from_telnet(self) -> None:
        """Implementation of Telnet update informations
        This method is only called by update method.
        And it's explains how to use TelnetConnection to get informations.
        """
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
