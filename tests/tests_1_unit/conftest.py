import pytest
from os import getcwd
from time import sleep

from atomic_p2p.peer import Peer
from atomic_p2p.utils.security import create_self_signed_cert as cssc

from yunnms.device import DeviceManager


@pytest.yield_fixture(scope='module')
def default_peer():
    p = Peer(host=('0.0.0.0', 8000), name='name', role='role',
             cert=cssc(getcwd(), 'data/test.pem', 'data/test.key'),
             _hash="THIS IS A HASH")
    p.start()

    yield p
    sleep(1)
    p.stop()


@pytest.yield_fixture(scope='module')
def default_device_manager(default_peer):
    d = DeviceManager(peer=default_peer)
    d.start()

    yield d
    sleep(1)
    d.stop()
