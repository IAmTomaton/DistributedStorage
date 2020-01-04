import os


class Data:

    def __init__(self, packer, unpacker, settings, number, path=""):
        self._packer = packer
        self._unpacker = unpacker
        self._settings = settings
        self._number = number
        self._value_file = os.path.join(path,
                                        "{}_value.txt".format(self._number))
        self._key_file = os.path.join(path,
                                      "{}_key.txt".format(self._number))
        with open(self._key_file, 'a') as f:
            pass
        with open(self._value_file, 'a') as f:
            pass
        self._load_keys()

    def _load_keys(self):
        self._keys = {}
        with open(self._key_file, 'r') as f:
            lines = f.read().splitlines()
            count = 0
            for line in lines:
                self._keys[line] = count
                count += 1

    def _get_value(self, key):
        with open(self._value_file, 'br') as f:
            count = self._keys[key]
            max_len = self._settings.max_len_value
            len_len = self._settings.len_len_value
            f.seek(count * (max_len + len_len))
            len_byte = f.read(self._settings.len_len_value)
            len = int.from_bytes(len_byte, "big")
            value = f.read(self._settings.max_len_value)[:len]
            return value.decode(self._settings.encoding)

    def _set_value(self, key, value):
        if key not in self._keys:
            count = len(self._keys)
            with open(self._key_file, 'a') as file_key:
                file_key.write("{}\n".format(key))
            self._keys[key] = count

        count = self._keys[key]
        value = value.encode(self._settings.encoding)
        with open(self._value_file, 'bw') as file_value:
            max_len = self._settings.max_len_value
            len_len = self._settings.len_len_value
            file_value.seek(count * (max_len + len_len))
            len_byte = (len(value)).to_bytes(self._settings.len_len_value,
                                             byteorder='big')
            file_value.write(len_byte)
            file_value.write(value)

    def clear(self):
        os.remove(self._value_file)
        os.remove(self._key_file)

    def handle_package(self, package, server):
        command, key, value = self._unpacker.parse_package(package)
        if command == "g":
            if key in self._keys:
                value = self._get_value(key)
                package = self._packer.create_set_package(key, value)
                server.send(package)
            else:
                server.send(self._packer.create_error_package_no_key(key))
        elif command == "s":
            self._set_value(key, value)
