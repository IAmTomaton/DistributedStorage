class Unpacker:

    def __init__(self, settings):
        self._settings = settings

    def parse_package(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        len_key = int.from_bytes(
            package[1:1 + self._settings.len_len_key], "big")
        key = package[1 + self._settings.len_len_key:
                      1 + self._settings.len_len_key + len_key]

        len_value_start = 1 + self._settings.len_len_key +\
            self._settings.max_len_key
        len_value_end = 1 + self._settings.len_len_key +\
            self._settings.max_len_key +\
            self._settings.len_len_value
        len_value = int.from_bytes(
            package[len_value_start: len_value_end], "big")

        value_start = 1 + self._settings.len_len_key +\
            self._settings.max_len_key +\
            self._settings.len_len_value
        value_end = 1 + self._settings.len_len_key +\
            self._settings.max_len_key +\
            self._settings.len_len_value + len_value
        value = package[value_start: value_end]

        str_key = key.decode(self._settings.encoding)
        str_value = value.decode(self._settings.encoding)

        return str_command, str_key, str_value

    def parse_number_package(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        if str_command != "n":
            return
        return int.from_bytes(package[1:5], "big")

    def parse_get_keys_package(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        if str_command != "f":
            return
        return int.from_bytes(package[1:5], "big")

    def parse_count_keys_package(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        if str_command != "c":
            return None, None
        number = int.from_bytes(package[1:5], "big")
        count = int.from_bytes(package[5:9], "big")
        return number, count

    def parse_keys_package(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        if str_command != "k":
            return None, None

        number = int.from_bytes(package[1:5], "big")
        count = int.from_bytes(package[5:6], "big")

        keys = []
        for i in range(count):
            start = 6 + 257 * i
            len_key = int.from_bytes(
                package[start:start + self._settings.len_len_key], "big")
            key = package[start + self._settings.len_len_key:
                          start + self._settings.len_len_key + len_key]
            keys.append(key.decode(self._settings.encoding)[1:])
        return number, keys

    def parse_command(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        return command

    def parse_number_data(self, package):
        return int.from_bytes(package[1:5], "big")
