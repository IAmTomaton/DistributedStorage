from multiprocessing import Manager


class Buffer:

    def __init__(self, unpacker):
        manager = Manager()
        self._buffer = manager.dict()
        self._unpacker = unpacker

    def get(self, key):
        while not key in self._buffer:
            pass
        return self._buffer[key]

    def handle_package(self, package):
        command, key, value = self._unpacker.parse_package(package)
        if command == "s":
            self._buffer[key] = value
