from logging import getLogger, basicConfig, DEBUG, Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler

from pysnmp.entity import config
from yunnms.device.entity.trap_server import TrapServer


log_format = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'

file_handler = TimedRotatingFileHandler(
    "./log/out.log",
    when="H",
    interval=1,
    encoding="utf-8",
    )
file_handler.setLevel(DEBUG)
file_handler.setFormatter(Formatter(log_format))

basicConfig(level=DEBUG, format=log_format)

logger = getLogger()
logger.addHandler(file_handler)
logger.setLevel(DEBUG)
ts = TrapServer(logger=logger)

authentications = [
    ("TestUser", "8000000903002C3F38E01D01"),
]

for (user_name, engine_id) in authentications:
    if user_name == "Test50":
        priv_protocol = config.usmNoPrivProtocol
        priv_key = None
    else:
        priv_protocol = config.usmDESPrivProtocol
        priv_key = "TestAuth"

    ts.addUser(authentication={
        'userName': user_name,
        'auth_protocol': config.usmHMACSHAAuthProtocol,
        'auth_key': 'TestAuth',
        'priv_protocol': priv_protocol,
        'priv_key': priv_key,
        'engineId': engine_id
    })

ts.start()

