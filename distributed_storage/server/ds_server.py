import socket
from threading import Thread
import select


class DSServer:

    def __init__(self, ip, port, handler, settings, packer, number):
        self._settings = settings
        self._ip = ip
        self._port = port
        self._handler = handler
        self._live = True
        self._number = number
        self._packer = packer
        self._thread = None

    def _work(self):
        while self._live:
            try:
                if self._connect():

                    self._sock.send(
                        self._packer.create_number_package(self._number))

                    while self._live:
                        try:
                            package = self._sock.recv(
                                self._settings.len_package)
                            if not package:
                                break
                            self._handler.handle_package(package, self)
                        except socket.timeout:
                            pass
            finally:
                try:
                    self._sock.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                self._sock.close()

    def start(self):
        self._live = True
        self._thread = Thread(target=self._work)
        self._thread.start()

    def _connect(self):
        while self._live:
            try:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.connect((self._ip, self._port))
                self._sock.settimeout(0.1)
                return True
            except ConnectionRefusedError:
                pass
        return False

    def send(self, package):
        self._sock.send(package)

    def turn_off(self):
        self._live = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
