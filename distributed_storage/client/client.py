from time import sleep
from distributed_storage.client.ds_client import DSClient
from distributed_storage.for_package.packer import Packer
from distributed_storage.for_package.unpacker import Unpacker
from distributed_storage.for_package.settings import Settings
from distributed_storage.client.buffer import Buffer
from distributed_storage.exceptions import NoRouterException


class Client:

    def __init__(self, ip, port, database_number=0):
        self._database_number = database_number

        settings = Settings()

        unpacker = Unpacker(settings)
        self._packer = Packer(settings)
        self._buffer = Buffer(unpacker)

        self._ds_client = DSClient(ip, port, self._buffer, settings)

    def set(self, key, value):
        key = str(self._database_number) + key
        self._check_connect()
        package = self._packer.create_set_package(key, value)
        self._ds_client.send(package)

    def get(self, key):
        key = str(self._database_number) + key
        self._check_connect()
        package = self._packer.create_get_package(key)
        self._ds_client.send(package)
        return self._buffer.get(key)

    def _check_connect(self):
        if not self._ds_client.connected:
            raise NoRouterException()

    def contains(self, key):
        return self._buffer.contains(key)

    def start(self):
        self._ds_client.start()

    def turn_off(self):
        self._ds_client.turn_off()
