from time import sleep
from distributed_storage.client.ds_client import DSClient
from distributed_storage.packages.packer import Packer
from distributed_storage.packages.unpacker import Unpacker
from distributed_storage.packages.settings import Settings
from distributed_storage.client.buffer import Buffer


class Client:

    def __init__(self, ip, port):
        settings = Settings()

        unpacker = Unpacker(settings)
        self._packer = Packer(settings)
        self._buffer = Buffer(unpacker)

        self._ds_client = DSClient(ip, port, self._buffer, settings)

    def set(self, key, value):
        self._check_sync()
        package = self._packer.create_set_package(key, value)
        self._ds_client.send(package)

    def get(self, key):
        self._check_sync()
        package = self._packer.create_get_package(key)
        self._ds_client.send(package)
        return self._buffer.get(key)

    def _check_sync(self):
        while not self._packer._settings.synchronized:
            sleep(0.1)

    def contains(self, key):
        return self._buffer.contains(key)

    def start(self):
        self._ds_client.start()

    def turn_off(self):
        self._ds_client.turn_off()
