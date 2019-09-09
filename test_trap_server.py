from pysnmp.entity import config
from yunnms.device.snmp import TrapServer

ts = TrapServer()

ts.addUser(authentication={
    'userName': 'TestUser',
    'auth_protocol': config.usmHMACSHAAuthProtocol,
    'auth_key': 'TestAuth',
    'priv_protocol': config.usmDESPrivProtocol, 'priv_key': 'TestAuth',
    'engineId': '800000090300FCFBFB0C3781'
})
ts.addUser(authentication={
    'userName': 'TestUser',
    'auth_protocol': config.usmHMACSHAAuthProtocol,
    'auth_key': 'TestAuth',
    'priv_protocol': config.usmDESPrivProtocol, 'priv_key': 'TestAuth',
    'engineId': '800000090300FCFBFB0C3781'
})
ts.addUser(authentication={
    'userName': 'TestUser',
    'auth_protocol': config.usmHMACSHAAuthProtocol,
    'auth_key': 'TestAuth',
    'priv_protocol': config.usmNoPrivProtocol, 'priv_key': None,
    'engineId': '8000000903000015FAD0B481'
})

ts.start()
