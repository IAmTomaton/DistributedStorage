from distributed_storage.packages.packer import Packer
from distributed_storage.packages.unpacker import Unpacker
from distributed_storage.packages.settings import Settings
from distributed_storage.server.ds_server import DSServer


class Server:

    def __init__(self, ip, port, number):
        self._settings = Settings()

        self._unpacker = Unpacker(self._settings)
        self._packer = Packer(self._settings)
        self._data = None
        self._ds_server = DSServer(ip, port, self._data, self._settings,
                                   self._packer, number)

    def start(self):
        self._ds_server.start()

    def turn_off(self):
        self._ds_server.turn_off()