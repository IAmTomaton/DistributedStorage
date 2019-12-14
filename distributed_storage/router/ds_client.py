import threading
import socket


class DSClient(threading.Thread):

    def __init__(self, conn, settings, manager):
        threading.Thread.__init__(self)
        self._conn = conn
        self._manager = manager
        self._live = True
        self._settings = settings

    def send(self, package):
        if (self._conn.fileno() != -1):
            self._conn.send(package)

    def _work(self):
        self._conn.timeout(0.1)
        while self._live:
            try:
                package = self._conn.recv(self._settings.len_package)
                self._manager.handle_package(package, self)
                if len(package) == 0:
                    self._live = False
                    break
            except socket.timeout:
                pass
        self._conn.close()

    def run(self):
        self._work()

    @property
    def live(self):
        return self._live
