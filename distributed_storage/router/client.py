from threading import Thread
import socket


class Client:

    def __init__(self, conn, settings, manager):
        self._conn = conn
        self._manager = manager
        self._live = True
        self._settings = settings
        self._thread = None
        self._connected = False

    @property
    def connected(self):
        return self._connected

    def send(self, package):
        if self.connected and self._live:
            self._conn.send(package)

    def _work(self):
        self._set_connected()
        self._conn.settimeout(0.1)
        self._live = True

        try:
            while self._live:
                try:
                    package = self._conn.recv(self._settings.len_package)
                    if len(package) == 0:
                        self._disconnected()
                        break
                    self._manager.handle_client_package(package, self)
                except socket.timeout:
                    pass
        finally:
            self._live = False
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self._conn.close()

    def start(self):
        self._live = True
        self._thread = Thread(target=self._work)
        self._thread.start()

    def turn_off(self):
        self._live = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _disconnected(self):
        self._connected = False

    def _set_connected(self):
        self._connected = True
