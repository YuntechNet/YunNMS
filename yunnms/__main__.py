from argparse import ArgumentParser

from atomic_p2p.local_monitor import LocalMonitor
from atomic_p2p.logging import getLogger

from yunnms import YunNMS


def min_length(data):
    if len(data) % 16 != 0:
        return data + " " * (16 - len(data) % 16)
    else:
        return data


parser = ArgumentParser()
parser.add_argument("address", help="Service's host address.")
parser.add_argument(
    "-t",
    "--target",
    default="127.0.0.1:8000",
    help="A peer address in Net.",
    dest="target",
)
parser.add_argument(
    "-c", "--cert", default="data/atomic_p2p.pem", help="Cert file path.", dest="cert"
)
parser.add_argument(
    "-as",
    "--auto-start",
    action="store_true",
    default=False,
    help="Auto start whole service.",
)
parser.add_argument(
    "-ajn",
    "--auto-join-net",
    action="store_true",
    default=False,
    help="Auto join a with Net address",
)
parser.add_argument(
    "-lmp",
    "--local-monitor-pass",
    dest="local_monitor_pass",
    default=None,
    type=min_length,
    help="Allow local monitor conntect",
)
args, left = parser.parse_known_args()

role = "core"
addr = args.address
target = args.target
name = "core"
cert = args.cert
auto_start = args.auto_start
auto_join_net = args.auto_join_net
local_monitor_pass = args.local_monitor_pass

logger = getLogger(name="AtomicP2P", add_monitor_pass=local_monitor_pass)
yunnms = YunNMS(addr=addr, name=name, cert=cert, ns=None, logger=logger)

if local_monitor_pass is not None:
    local_monitor = LocalMonitor(
        service=yunnms, password=local_monitor_pass, logger=logger
    )
    yunnms.local_monitor = local_monitor

if auto_start is True:
    yunnms.start()

if auto_join_net is True and target is not None:
    if auto_start is False:
        yunnms.start()

    yunnms.peer.join_net(host=(addr[0], addr[1]))
