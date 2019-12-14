from distributed_storage.client.ds_client import DSClient
from distributed_storage.packages.packer import Packer
from distributed_storage.packages.unpacker import Unpacker
from distributed_storage.packages.settings import Settings
from distributed_storage.client.client import Client
from distributed_storage.client.buffer import Buffer


class ClientManager:

    def __init__(self, ip, port):
        settings = Settings(2048)

        unpacker = Unpacker(settings)
        packer = Packer(settings)
        buffer = Buffer(unpacker)

        ds_client = DSClient(ip, port, buffer, settings)

        self._client = Client(packer, buffer, ds_client)

    def __enter__(self):
        self._client._start()
        return self._client

    def __exit__(self, type, value, traceback):
        self._client._stop()
