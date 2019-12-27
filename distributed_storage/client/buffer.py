from time import sleep
from threading import Lock


class Buffer:

    def __init__(self, unpacker):
        self._buffer = {}
        self._errors = {}
        self._buffer_lock = Lock()
        self._unpacker = unpacker

    def get(self, key):
        check = not(key in self._buffer or key in self._errors)
        while check:
            check = not(key in self._buffer or key in self._errors)
            sleep(0.1)
        self._buffer_lock.acquire()
        try:
            value = self._buffer.pop(key, None)
            error = self._errors.pop(key, None)
        finally:
            self._buffer_lock.release()
        return value, error

    def contains(self, key):
        return key in self._buffer

    def handle_package(self, package):
        command, key, value = self._unpacker.parse_package(package)
        self._buffer_lock.acquire()
        try:
            if command == "s":
                self._buffer[key] = value
            if command == "y":
                self._unpacker.parse_sync_package(package)
            if command == "e":
                self._errors[key] = value
        finally:
            self._buffer_lock.release()
