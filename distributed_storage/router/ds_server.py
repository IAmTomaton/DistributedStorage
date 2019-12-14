import threading
from multiprocessing import Manager


class DSServer(threading.Thread):

    def __init__(self, conn, settings, manager, applications):
        threading.Thread.__init__(self)
        self._conn = conn
        self._manager = manager
        self._applications = applications
        manager = Manager()
        self._orders = manager.list()
        self._live = True
        self._settings = settings

    def add_order(self, order):
        self._orders.append(order)

    def send(self, package):
        if (self._conn.fileno() != -1):
            self._conn.send(package)

    def _handle_package(self, package):
        pass

    def _work(self):
        self._conn.timeout(0.1)
        while self._live:
            try:
                package = self._conn.recv(self._settings.len_package)
                if len(package) == 0:
                    self._live = False
                    break
            except socket.timeout:
                pass
        self._conn.close()

    def run(self):
        pass

    @property
    def live(self):
        return self._live
