from time import sleep
from threading import Lock
from distributed_storage.exceptions import DSException
from distributed_storage.exceptions import NoServerException
from distributed_storage.exceptions import NoKeyException


class Buffer:

    def __init__(self, unpacker):
        self._buffer = {}
        self._errors = {}
        self._buffer_lock = Lock()
        self._unpacker = unpacker
        self._keys = []

    def get(self, key):
        if not(key in self._buffer or key in self._errors):
            raise KeyError(
                "A package for this key has not yet arrived or a request \
has not been sent")
        self._buffer_lock.acquire()
        try:
            error = self._errors.pop(key, None)
            if error == "ns":
                raise NoServerException(key)
            elif error == "nk":
                raise NoKeyException(key)
            value = self._buffer.pop(key, None)
            if value is None:
                raise DSException(
                    "There was no key error, but for some reason there is \
no value in the buffer[unkown error]")
            return value
        finally:
            self._buffer_lock.release()

    def contains(self, key):
        return key in self._buffer or key in self._errors

    def handle_package(self, package):
        command, key, value = self._unpacker.parse_package(package)
        self._buffer_lock.acquire()
        try:
            if command == "s":
                self._buffer[key] = value
            if command == "e":
                self._errors[key] = value
            if command == "k":
                number, keys = self._unpacker.parse_keys_package(package)
                for key in keys:
                    if key not in self._keys:
                        self._keys.append(key)
        finally:
            self._buffer_lock.release()

    def keys(self):
        self._buffer_lock.acquire()
        try:
            return self._keys
        finally:
            self._buffer_lock.release()

    def reset_keys(self):
        self._keys = []
