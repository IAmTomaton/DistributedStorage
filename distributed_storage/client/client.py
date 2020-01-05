from time import sleep
from distributed_storage.client.ds_client import DSClient
from distributed_storage.for_package.packer import Packer
from distributed_storage.for_package.unpacker import Unpacker
from distributed_storage.for_package.settings import Settings
from distributed_storage.client.buffer import Buffer
from distributed_storage.exceptions import NoRouterException
from distributed_storage.exceptions import LenKeyException
from distributed_storage.exceptions import LenValueException


class Client:

    def __init__(self, ip, port, database_number=0):
        settings = Settings()

        unpacker = Unpacker(settings)
        self._packer = Packer(settings)
        self._buffer = Buffer(unpacker)

        self._ds_client = DSClient(ip, port, self._buffer, settings)
        self._database_number = ((database_number).to_bytes(
            1, byteorder='big')).decode(settings.encoding)

    def set(self, key, value):
        self._check_key(key)
        self._check_value(value)
        key = self._database_number + key
        self._check_connect()
        package = self._packer.create_set_package(key, value)
        self._ds_client.send(package)

    def send_get(self, key):
        self._check_key(key)
        key = self._database_number + key
        self._check_connect()
        package = self._packer.create_get_package(key)
        self._ds_client.send(package)

    def get(self, key):
        self._check_key(key)
        key = self._database_number + key
        return self._buffer.get(key)

    def _check_connect(self):
        if not self._ds_client.connected:
            raise NoRouterException()

    def _check_key(sekf, key):
        if len(key) > 250:
            raise LenKeyException(key)

    def _check_value(sekf, value):
        if len(value) > 1200:
            raise LenValueException(value)

    def contains(self, key):
        return self._buffer.contains(key)

    def start(self):
        self._ds_client.start()

    def turn_off(self):
        self._ds_client.turn_off()

    def send_get_keys(self,):
        self._check_connect()
        self._buffer.reset_keys()
        package = self._packer.create_get_keys_package(self._database_number)
        self._ds_client.send(package)

    def keys(self):
        return self._buffer.keys()
