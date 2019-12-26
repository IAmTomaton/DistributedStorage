import socket
import threading


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
        self._sock = socket.socket()
        
        try:
            while self._live:
                self._connect()

                self._sock.send(self._packer.create_number_package(
                    self._number))

                while self._live:
                    try:
                        package = self._sock.recv(self._settings.len_package)
                        if len(package) == 0:
                            break
                        #print(package)
                        #self._handler.handle_package(package)
                    except socket.timeout:
                        pass
        finally:
            self._live = False
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
                break
            except ConnectionRefusedError:
                pass

    def send(self, package):
        self._sock.send(package)

    def turn_off(self):
        self._live = False
