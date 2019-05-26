import re
from pysnmp.hlapi.asyncore import *


class Interface(object):

    def __init__(self, name, status=None, snmp_index=-1):
        self.name = name
        self.status = status
        self.snmp_index = int(snmp_index)

    def __str__(self):
        return 'Interface<snmp_index={}, name={}, status={}>'.format(
            self.snmp_index, self.name, self.status)
