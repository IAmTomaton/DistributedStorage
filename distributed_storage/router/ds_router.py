import threading
import socket


class DSRouter(threading.Thread):

    def __init__(self, ip, port, manager):
        threading.Thread.__init__(self)
        self._ip = ip
        self._port = port
        self._manager = manager
        self._live = True

    def accept_connections(self):
        sock = socket.socket()
        sock.bind((self._ip, self._port))

        sock.timeout(1)

        while self._live:
            try:
                conn, addr = sock.accept()
                self._manager.connect(conn. addr)
            except socket.timeout:
                pass

    def run(self):
        self.accept_connections()
