import pytest
from os import getcwd
from time import sleep

from atomic_p2p.peer import ThreadPeer
from atomic_p2p.utils.security import create_self_signed_cert as cssc

from yunnms.device import DeviceManager


@pytest.yield_fixture(scope='module')
def default_peer():
    p = ThreadPeer(host=('0.0.0.0', 8000), name='name', role='role',
             cert=cssc(getcwd(), 'data/test.pem', 'data/test.key'),
             program_hash="THIS IS A HASH", ns=None)
    p.start()

    yield p
    sleep(1)
    p.stop()


@pytest.yield_fixture(scope='module')
def default_device_manager(default_peer):
    # trap_host should be ("0.0.0.0", 162) but due to Travis sudo.
    # We need to use host & port which not touched system restrict.
    d = DeviceManager(peer=default_peer, trap_host=("127.0.0.1", 10162))
    d.start()

    yield d
    sleep(1)
    d.stop()
