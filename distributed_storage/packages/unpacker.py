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

        len_value = int.from_bytes(
            package[1 + self._settings.len_len_key +\
                self._settings.max_len_key:
                    1 + self._settings.len_len_key +\
                self._settings.max_len_key +\
                self._settings.len_len_value], "big")
        value = package[1 + self._settings.len_len_key +\
                self._settings.max_len_key +\
                self._settings.len_len_value:
                      1 + self._settings.len_len_key +\
                self._settings.max_len_key +\
                self._settings.len_len_value + len_value]

        str_key = key.decode(self._settings.encoding)
        str_value = value.decode(self._settings.encoding)

        return str_command, str_key, str_value

    def parse_sync_package(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        if str_command != "y":
            return
        max_len_value = int.from_bytes(package[1:5], "big")
        self._settings.max_len_value = max_len_value

    def parse_number_package(self, package):
        command = package[0:1]
        str_command = command.decode(self._settings.encoding)

        if str_command != "n":
            return
        return int.from_bytes(package[1:5], "big")
