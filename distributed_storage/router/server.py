from threading import Lock, Thread
import socket


class Server:

    def __init__(self, settings, manager, packer, unpacker, number):
        self._manager = manager
        self._settings = settings
        self._packer = packer
        self._unpacker = unpacker
        self._number = number
        self._conn = None
        self._live = False
        self._lock = Lock()
        self._thread = None
        self._connected = False

    @property
    def connected(self):
        return self._connected

    def send(self, package):
        self._lock.acquire()
        try:
            if self.connected and self._live:
                self._conn.send(package)
        finally:
            self._lock.release()

    def connect(self, conn):
        self._conn = conn
        self.start()

    def _work(self):
        self._set_connected()
        self._live = True
        self._conn.settimeout(0.1)

        try:
            while self._live:
                try:
                    package = self._conn.recv(self._settings.len_package)
                    if not package:
                        self._disconnected()
                        break
                    self._manager.handle_server_package(package,
                                                        self._number)
                except socket.timeout:
                    pass
        finally:
            self._live = False
            self._lock.acquire()
            try:
                sock.shutdown(socket.SHUT_RDWR)
                self._conn.close()
                self._conn = None
            finally:
                self._lock.release()
            self._manager.skip_orders(self._number)

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
