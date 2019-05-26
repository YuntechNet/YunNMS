

class DeviceInfo(object):

    def __init__(self) -> None:
        pass

    def update(self) -> None:
        raise NotImplementedError

    def __update_from_snmp_v3(self, snmp_conn: 'SNMPv3Connection') -> None:
        raise NotImplementedError

    def __update_from_ssh(self, ssh_conn: 'SSHConnection') -> None:
        raise NotImplementedError

    def __update_from_telnet(self, telnet_conn: 'TelnetConnection') -> None:
        raise NotImplementedError
