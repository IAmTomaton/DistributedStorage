class Data:

    def __init__(self, packer, unpacker):
        self._packer = packer
        self._unpacker = unpacker
        self._data = {}

    def handle_package(self, package, server):
        command, key, value = self._unpacker.parse_package(package)
        if command == "g":
            if key in self._data:
                server.send(self._packer.create_set_package(key,
                                                            self._data[key]))
            else:
                server.send(self._packer.create_error_package_not_key(key))
        elif command == "s":
            self._data[key] = value
