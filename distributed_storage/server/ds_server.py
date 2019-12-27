import socket
import threading
import select


class DSServer(threading.Thread):

    def __init__(self, ip, port, handler, settings, packer, number):
        threading.Thread.__init__(self)
        self._settings = settings
        self._ip = ip
        self._port = port
        self._handler = handler
        self._live = True
        self._number = number
        self._packer = packer

    def _work(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    def run(self):
        self._work()

    def _connect(self):
        while self._live:
            try:
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
