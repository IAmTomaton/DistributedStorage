from distributed_storage.router.server import Server
from distributed_storage.router.client import Client
from distributed_storage.router.order import Order
from distributed_storage.router.orders import Orders
from threading import Lock


class Manager:

    def __init__(self, packer, unpacker, settings, number_servers):
        self._packer = packer
        self._unpacker = unpacker
        self._settings = settings
        self._amount_duplication = 2
        self._clients = []

        self._number_servers = number_servers
        self._application_table = []
        self._application_lock = Lock()
        self._order_table = []
        self._server_table = []
        for i in range(self._number_servers):
            self._application_table.append([])
            self._order_table.append(Orders())
            self._server_table.append(Server(self._settings,
                                             self,
                                             self._packer,
                                             self._unpacker,
                                             i))

    def add_server(self, conn, addr, number):
        self._server_table[number].connect(conn)

        self._application_lock.acquire()
        try:
            self._update_application_table()
        finally:
            self._application_lock.release()

    def _update_application_table(self):
        for i in range(self._number_servers):
            server = self._server_table[i]
            buffer = []
            for key in self._application_table[i]:
                get_package = self._packer.create_get_package(key)
                count = self._create_order(key, get_package, server)
                if count == 0:
                    buffer.append(key)
            self._application_table[i] = buffer

    def add_client(self, conn, addr):
        client = Client(conn, self._settings, self)
        self._clients.append(client)
        client.start()

    def handle_client_package(self, package, customer):
        command, key, value = self._unpacker.parse_package(package)
        if command == "g":
            count = self._create_order(key, package, customer)
            if count == 0:
                customer.send(
                    self._packer.create_error_package_no_server(key))
        elif command == "s":
            self._send_set_package(package, key)

    def _send_set_package(self, package, key):
        hash = self._get_hash(key)

        for i in range(self._amount_duplication):
            index_server = (hash + i) % self._number_servers
            self.try_send_set_package(index_server, key, package)

    def try_send_set_package(self, index_server, key, package):
        if self._server_table[index_server].connected:
            self._server_table[index_server].send(package)
        else:
            self._add_application(key, index_server)

    def _add_application(self, key, index):
        self._application_lock.acquire()
        try:
            self._application_table[index].append(key)
        finally:
            self._application_lock.release()

    def _create_order(self, key, package, customer):
        hash = self._get_hash(key)
        order = Order(key, customer)

        for i in range(self._amount_duplication):
            index_server = (hash + i) % self._number_servers
            conn = self._server_table[index_server].connected
            if self._server_table[index_server] != customer and conn:

                self._add_order(order, index_server)
                self._server_table[index_server].send(package)
        return order.count

    def _add_order(self, order, index):
        self._order_table[index].add_order(order)

    def handle_server_package(self, package, number):
        command, key, value = self._unpacker.parse_package(package)
        self._order_table[number].send(command, key, package, number,
                                       self._packer, self)

    def _get_hash(self, key):
        number = 11
        sum = 0
        for i in key:
            sum = int.from_bytes(i.encode('utf-8'), "big") + sum * number
        return sum % self._number_servers

    def skip_orders(self, index):
        self._order_table[index].skip()

    def turn_off(self):
        for client in self._clients:
            client.turn_off()
        for server in self._server_table:
            server.turn_off()
