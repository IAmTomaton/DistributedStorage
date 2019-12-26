import threading
import socket


class Client(threading.Thread):

    def __init__(self, conn, settings, manager):
        threading.Thread.__init__(self)
        self._conn = conn
        self._manager = manager
        self._live = True
        self._settings = settings

    def send(self, package):
        if (self._conn.fileno() != -1 and self._live):
            self._conn.send(package)

    def _work(self):
        self._conn.timeout(0.1)
        try:
            while self._live:
                try:
                    package = self._conn.recv(self._settings.len_package)
                    if len(package) == 0:
                        break
                    self._manager.handle_client_package(package, self)
                except socket.timeout:
                    pass
        finally:
            self._live = False
            self._conn.shutdown(socket.SHUT_RDWR)
            self._conn.close()

    def run(self):
        self._work()

    @property
    def live(self):
        return self._live
