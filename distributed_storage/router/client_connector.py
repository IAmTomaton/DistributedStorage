import threading
import socket


class ClientConnector(threading.Thread):

    def __init__(self, ip, port, manager, packer):
        threading.Thread.__init__(self)
        self._ip = ip
        self._port = port
        self._manager = manager
        self._packer = packer
        self._live = False

    def _disconnect(self):
        self._conn.shutdown(socket.SHUT_RDWR)
        self._conn.close()
        self._conn = None

    def _accept_connections(self):
        sock = socket.socket()
        sock.bind((self._ip, self._port))

        sock.timeout(1)

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
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

    def run(self):
        self._accept_connections()



