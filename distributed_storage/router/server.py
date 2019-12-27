import threading
from threading import Lock
import socket


class Server(threading.Thread):

    def __init__(self, settings, manager, packer, unpacker, number):
        threading.Thread.__init__(self)
        self._manager = manager
        self._settings = settings
        self._packer = packer
        self._unpacker = unpacker
        self._number = number
        self._conn = None
        self._live = False
        self._lock = Lock()

    @property
    def connected(self):
        return self._conn is not None and\
            self._conn.fileno() != -1

    def send(self, package):
        self._lock.acquire()
        try:
            if (self._conn is not None and\
                self._conn.fileno() != -1 and\
                self._live):
                self._conn.send(package)
        finally:
            self._lock.release()

    def connect(self, conn):
        self._conn = conn
        self.start()

    def _work(self):
        self._conn.settimeout(0.1)
        self._live = True
        try:
            while self._live:
                try:
                    package = self._conn.recv(self._settings.len_package)
                    if len(package) == 0:
                        break
                    self._manager.handle_server_package(package,
                                                        self._number)
                except socket.timeout:
                    pass
        finally:
            self._live = False
            self._lock.acquire()
            try:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                self._conn.close()
                self._conn = None
            finally:
                self._lock.release()
            self._manager.skip_orders(self._number)

    def run(self):
        self._work()

    def turn_off(self):
        self._live = False
