from distributed_storage.router.server import Server
from distributed_storage.router.ds_server import DSServer
from distributed_storage.router.ds_client import DSClient


class Manager:

    def __init__(self, server_addresses, packer, unpacker, settings,
                 max_len_value):
        self._server_addresses = server_addresses
        self._init_servers()
        self._clients = []
        self._packer = packer
        self._unpacker = unpacker
        self._max_len_value = max_len_value
        self._settings = settings

    def _init_servers(self):
        self._servers = []
        self._servers_dict = {}
        for i in range(len(self._server_addresses)):
            self._servers.append(Server())
            self._servers_dict[self._server_addresses[i]] = i

    def connect(self, conn, addr):
        if addr in self._server_addresses:
            self._add_server(conn, addr)
        else:
            self._add_client(conn, addr)

    def _add_server(self, conn, addr):
        server = self._servers[self._servers_dict[addr]]
        ds_server = DSServer(conn, self._settings, self, server.applications)
        server.ds_server = ds_server
        ds_server.start()
        ds_server.send(self._get_sync_package())

    def _add_client(self, conn, addr):
        ds_client = DSClient(conn, self._settings, self)
        self._clients.append(ds_client)
        ds_client.start()
        ds_client.send(self._get_sync_package())

    def clear(self):
        i = 0
        while i < len(self._clients):
            if not self._clients[i].live:
                self._clients.pop(i)
            else:
                i += 1
        for s in self._servers:
            if not s.ds_server.live:
                s.ds_server = None

    def handle_package(self, package, customer):
        pass

    def _get_sync_package(self):
        return self._packer.create_sync_package(self._max_len_value)
