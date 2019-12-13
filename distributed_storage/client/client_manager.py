from distributed_storage.client.ds_client import DSClient
from distributed_storage.client.packer import Packer
from distributed_storage.client.unpacker import Unpacker
from distributed_storage.client.settings import Settings
from distributed_storage.client.client import Client


class ClientManager:

    def __init__(self, ip, port):
        settings = Settings(2048)

        handler = Unpacker(settings)
        packer = Packer(settings)
        ds_client = DSClient(ip, port, handler, settings)

        self._client = Client(packer, ds_client)

    def __enter__(self):
        self._client._start()
        return self._client

    def __exit__(self, type, value, traceback):
        self._client._stop()
