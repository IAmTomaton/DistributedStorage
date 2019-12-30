from threading import Thread
import socket


class ServerConnector:

    def __init__(self, ip, port, manager, settings, packer, unpacker):
        self._ip = ip
        self._port = port
        self._manager = manager
        self._settings = settings
        self._packer = packer
        self._unpacker = unpacker
        self._live = False
        self._thread = None

    def _accept_connections(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self._ip, self._port))
        sock.listen(1)

        sock.settimeout(0.1)

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
        check = True
        try:
            conn.send(self._packer.create_sync_package())
            conn.settimeout(0.1)
            while self._live:
                try:
                    package = conn.recv(self._settings.standart_len_package)
                    if not package:
                        break
                    number = self._unpacker.parse_number_package(package)
                    self._manager.add_server(conn, addr, number)
                    check = False
                    return
                except socket.timeout:
                    pass
        finally:
            if check:
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                conn.close()

    def start(self):
        self._live = True
        self._thread = Thread(target=self._accept_connections)
        self._thread.start()

    def turn_off(self):
        self._live = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
