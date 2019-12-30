from threading import Thread
import socket


class ClientConnector:

    def __init__(self, ip, port, manager, packer):
        self._ip = ip
        self._port = port
        self._manager = manager
        self._packer = packer
        self._live = False
        self._thread = None

    def _accept_connections(self):
        sock = socket.socket()
        sock.bind((self._ip, self._port))
        sock.listen(1)

        sock.settimeout(0.1)

        self._live = True
        try:
            while self._live:
                try:
                    conn, addr = sock.accept()
                    conn.send(self._packer.create_sync_package())
                    self._manager.add_client(conn, addr)
                except socket.timeout:
                    pass
        finally:
            self._live = False
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            sock.close()

    def start(self):
        self._live = True
        self._thread = Thread(target=self._accept_connections)
        self._thread.start()

    def turn_off(self):
        self._live = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
