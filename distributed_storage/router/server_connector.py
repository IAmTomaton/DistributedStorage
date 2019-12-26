import threading
import socket


class ServerConnector(threading.Thread):

    def __init__(self, ip, port, manager, settings, packer, unpacker):
        threading.Thread.__init__(self)
        self._ip = ip
        self._port = port
        self._manager = manager
        self._settings = settings
        self._packer = packer
        self._unpacker = unpacker
        self._live = False

    def _accept_connections(self):
        sock = socket.socket()
        sock.bind((self._ip, self._port))
        sock.listen(1)

        sock.settimeout(1)

        self._live = True
        try:
            while self._live:
                try:
                    self._accept(sock)
                except socket.timeout:
                    pass
        finally:
            self._live = False
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            sock.close()

    def _accept(self, sock):
        conn, addr = sock.accept()
        try:
            conn.send(self._packer.create_sync_package())
            conn.settimeout(0.1)
            while self._live:
                try:
                    package = conn.recv(self._settings.standart_len_package)
                    if len(package) == 0:
                        break
                    number = self._unpacker.parse_number_package(package)
                    self._manager.add_server(conn, addr, number)
                    break
                except socket.timeout:
                    pass
        finally:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            conn.close()

    def run(self):
        self._accept_connections()

    def turn_off(self):
        self._live = False
