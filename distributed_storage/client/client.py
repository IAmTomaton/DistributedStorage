class Client:

    def __init__(self, packer, ds_client):
        self._packer = packer
        self._ds_client = ds_client

    def set(self, key, value):
        package = self._packer.create_set_package(key, value)
        self._ds_client.send(package)

    def get(self, key):
        package = self._packer.create_get_package(key)
        self._ds_client.send(package)

    def _start(self):
        self._ds_client.start()

    def _stop(self):
        self._ds_client.stop()
