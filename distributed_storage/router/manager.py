from distributed_storage.router.server import Server
from distributed_storage.router.ds_server import DSServer
from distributed_storage.router.ds_client import DSClient
from distributed_storage.router.order import Order


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
        self._amount_duplication = 2

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
        command, key, value = self._unpacker.parse_package(package)
        if command == "g":
            self._create_order(key, customer)
        elif command == "s":
            self._send_set_package(package, key)

    def _send_set_package(self, package, key):
        hash = self._get_hash(key)

        for i in range(self._amount_duplication):
            index_server = (hash + i) % len(self._server_addresses)
            if self._servers[index_server].is_connected:
                self._servers[index_server].ds_server.send(package)
            else:
                self._servers[index_server].applications.put(key)

    def _create_order(self, key, customer):
        hash = self._get_hash(key)
        order = Order(key, customer)

        for i in range(self._amount_duplication):
            index_server = (hash + i) % len(self._server_addresses)
            if self._servers[index_server].is_connected:
                self._servers[index_server].add_order(order)

    def _get_hash(self, key):
        number = 11
        sum = 0
        for i in key:
            sum = int.from_bytes(i.encode('utf-8'), "big") + sum * number
        return sum % len(self._server_addresses)

    def _get_sync_package(self):
        return self._packer.create_sync_package(self._max_len_value)
