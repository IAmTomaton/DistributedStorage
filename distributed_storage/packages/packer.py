class Packer:

    def __init__(self, settings):
        self._settings = settings
        
    def create_get_package(self, key):
        package = bytearray(b'g')

        key_byte = bytearray(key.encode(self._settings.encoding))
        len_key = len(key_byte)
        key_package = key_byte + bytearray(b'\x00') *\
            (self._settings.max_len_key - len_key)
        len_key_package = bytearray((len_key).to_bytes(
            self._settings.len_len_key,
            byteorder='big'))

        package += len_key_package
        package += key_package

        value = bytearray(b'\x00') *\
            (self._settings.len_len_value + self._settings.max_len_value)

        package += value

        return bytes(package)

    def create_set_package(self, key, value):
        package = bytearray(b's')

        key_byte = bytearray(key.encode(self._settings.encoding))
        len_key = len(key_byte)
        key_package = key_byte + bytearray(b'\x00') *\
            (self._settings.max_len_key - len_key)
        len_key_package = bytearray((len_key).to_bytes(
            self._settings.len_len_key,
            byteorder='big'))

        package += len_key_package
        package += key_package

        value_byte = bytearray(value.encode(self._settings.encoding))
        len_value = len(value_byte)
        value_package = value_byte + bytearray(b'\x00') *\
            (self._settings.max_len_value - len_value)
        len_value_package = bytearray((len_value).to_bytes(
            self._settings.len_len_value,
            byteorder='big'))

        package += len_value_package
        package += value_package

        return bytes(package)

    def create_sync_package(self):
        package = bytearray(b'y')

        package += bytearray((self._settings.max_len_value).to_bytes(4, byteorder='big'))

        package += bytearray(b'\x00') * (self._settings.standart_len_package - 5)

        return bytes(package)

    def create_number_package(self, number):
        package = bytearray(b'n')

        package += bytearray((max_len_value).to_bytes(4, byteorder='big'))

        package += bytearray(b'\x00') * (self._settings.len_package - 2)

        return bytes(package)

    def create_error_package(self, key, text):
        package = bytearray(b'e')

        key_byte = bytearray(key.encode(self._settings.encoding))
        len_key = len(key_byte)
        key_package = key_byte + bytearray(b'\x00') *\
            (self._settings.max_len_key - len_key)
        len_key_package = bytearray((len_key).to_bytes(
            self._settings.len_len_key,
            byteorder='big'))

        package += len_key_package
        package += key_package

        value_byte = bytearray(text.encode(self._settings.encoding))
        len_value = len(value_byte)
        value_package = value_byte + bytearray(b'\x00') *\
            (self._settings.max_len_value - len_value)
        len_value_package = bytearray((len_value).to_bytes(
            self._settings.len_len_value,
            byteorder='big'))

        package += len_value_package
        package += value_package

        return bytes(package)

    def create_error_package_not_server(self, key):
        text = "server storing key disabled"
        return self.create_error_package(key, text)

    def create_error_package_not_key(self, key):
        text = "the key does not exist"
        return self.create_error_package(key, text)
