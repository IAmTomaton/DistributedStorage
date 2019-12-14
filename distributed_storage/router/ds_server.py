import threading
from multiprocessing import Manager


class DSServer(threading.Thread):

    def __init__(self, conn, settings, manager, applications, packer, unpacker):
        threading.Thread.__init__(self)
        self._conn = conn
        self._manager = manager
        self._applications = applications
        manager = Manager()
        self._orders = manager.list()
        self._live = True
        self._settings = settings
        self._packer = packer
        self._unpacker = unpacker

    def add_order(self, order):
        self._orders.append(order)

    def send(self, package):
        if (self._conn.fileno() != -1):
            self._conn.send(package)

    def _handle_package(self, package):
        command, key, value = self._unpacker.parse_package(package)
        if command != "s":
            return
        i = 0
        while i < len(self._orders):
            order = self._orders[i]
            order.send(package)
            if order.is_completed:
                self._orders.pop(i)
            else:
                i += 1

    def _work(self):
        self._conn.timeout(0.1)
        while self._live:
            try:
                package = self._conn.recv(self._settings.len_package)
                if len(package) == 0:
                    self._live = False
                    break
                self._handle_package(package)
            except socket.timeout:
                pass
        self._conn.close()

    def _handle_applications(self):
        for a in self._applications:
            get = self._packer.create_get_package(a)
            self._manager.handle_package(get, self)

    def run(self):
        self._handle_applications()
        self._work()

    @property
    def live(self):
        return self._live
