import socket
import threading
from distributed_storage.exeptions.connect_exeption import ConnectExeption


class DSClient(threading.Thread):

    def __init__(self, ip, port, handler, settings):
        threading.Thread.__init__(self)
        self._settings = settings
        self._ip = ip
        self._port = port
        self._handler = handler
        self._live = True

    def _handle_package(self, package):
        self._handler.handle_package(package)

    def _work(self):
        self._sock = socket.socket()
        
        self._connect()
        self._sock.timeout(0.1)

        while self._live:
            try:
                package = self._sock.recv(self._settings.len_package)
                if len(package) == 0:
                    self._live = False
                    break
                self._handle_package(package)
            except socket.timeout:
                pass

        self._sock.close()

    def run(self):
        self._work()

    def _connect(self):
        try:
            self._sock.connect((self._ip, self._port))
        except ConnectionRefusedError:
            raise ConnectExeption("Server is not responding.")

    def send(self, package):
        self._sock.send(package)

    def stop(self):
        self._live = False
