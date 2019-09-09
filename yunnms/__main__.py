from argparse import ArgumentParser
from os import getcwd

from atomic_p2p.peer.communication.net import JoinHandler

from yunnms import YunNMS

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
args, left = parser.parse_known_args()

role = "core"
addr = args.address
target = args.target
name = "core"
cert = args.cert
auto_start = args.auto_start
auto_join_net = args.auto_join_net

yunnms = YunNMS(addr=addr, name=name, cert=cert, ns=None)

if auto_start is True:
    yunnms.start()

if auto_join_net is True and target is not None:
    if auto_start is False:
        yunnms.start()

    yunnms.peer.join_net(host=(addr[0], addr[1]))
