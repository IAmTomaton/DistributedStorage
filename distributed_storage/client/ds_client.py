import socket
import threading


class DSClient(threading.Thread):

    def __init__(self, ip, port, handler, settings):
        threading.Thread.__init__(self)
        self._settings = settings
        self._ip = ip
        self._port = port
        self._hendler = hendler
        self._live = True

    def run(self):
        sock = socket.socket()
        sock.connect((self._ip, self._port))
        while self._live:
            pass
        sock.close()

    def send(self, package):
        pass

    def stop(self):
        self._live = False
