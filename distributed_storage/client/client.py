from time import sleep


class Client:

    def __init__(self, packer, buffer, ds_client):
        self._packer = packer
        self._buffer = buffer
        self._ds_client = ds_client

    def set(self, key, value):
        self.check_sync()
        package = self._packer.create_set_package(key, value)
        self._ds_client.send(package)

    def get(self, key):
        self.check_sync()
        package = self._packer.create_get_package(key)
        self._ds_client.send(package)
        return self._buffer.get(key)

    def check_sync(self):
        while not self._packer._settings.synchronized:
            sleep(0.1)

    def _start(self):
        self._ds_client.start()

    def _stop(self):
        self._ds_client.stop()
