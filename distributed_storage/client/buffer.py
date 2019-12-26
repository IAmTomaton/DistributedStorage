from time import sleep
from threading import Lock


class Buffer:

    def __init__(self, unpacker):
        self._buffer = {}
        self._buffer_lock = Lock()
        self._unpacker = unpacker

    def get(self, key):
        while not key in self._buffer:
            sleep(0.1)
        self._buffer_lock.acquire()
        try:
            value = self._buffer[key]
        finally:
            self._buffer_lock.release()
        return value

    def handle_package(self, package):
        command, key, value = self._unpacker.parse_package(package)
        if command == "s":
            self._buffer[key] = value
