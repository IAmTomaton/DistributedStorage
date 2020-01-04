from distributed_storage.for_package.packer import Packer
from distributed_storage.for_package.unpacker import Unpacker
from distributed_storage.for_package.settings import Settings
from distributed_storage.server.ds_server import DSServer
from distributed_storage.server.data import Data


class Server:

    def __init__(self, ip, port, number, path=""):
        self._settings = Settings()

        self._unpacker = Unpacker(self._settings)
        self._packer = Packer(self._settings)
        self._data = Data(self._packer, self._unpacker, self._settings,
                          number, path)
        self._ds_server = DSServer(ip, port, self._data, self._settings,
                                   self._packer, number)

    def start(self):
        self._ds_server.start()

    def turn_off(self):
        self._ds_server.turn_off()

    def clear(self):
        self._data.clear()
