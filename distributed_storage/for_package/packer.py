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

    def create_number_package(self, number):
        package = bytearray(b'n')

        package += bytearray((number).to_bytes(4, byteorder='big'))

        package += bytearray(b'\x00') * (self._settings.len_package - 5)

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

    def create_error_package_no_key(self, key):
        return self.create_error_package(key, "nk")

    def create_error_package_no_server(self, key):
        return self.create_error_package(key, "ns")

    def create_get_keys_package(self, number):
        package = bytearray(b'f')

        package += bytearray(number.encode(self._settings.encoding))

        package += bytearray(b'\x00') * (self._settings.len_package - 2)

        return bytes(package)

    def create_count_keys_package(self, number, count):
        package = bytearray(b'c')

        package += bytearray(number)
        package += bytearray((count).to_bytes(4, byteorder='big'))

        package += bytearray(b'\x00') * (self._settings.len_package - 6)

        return bytes(package)

    def create_keys_package(self, number, keys):
        package = bytearray(b'k')

        package += bytearray(number)
        package += bytearray((len(keys)).to_bytes(1, byteorder='big'))
        count = 0
        for i in range(len(keys)):
            count += 1
            key = keys[i]
            key_byte = bytearray(key.encode(self._settings.encoding))
            len_key = len(key_byte)
            key_package = key_byte + bytearray(b'\x00') *\
                (self._settings.max_len_key - len_key)
            len_key_package = bytearray((len_key).to_bytes(
                self._settings.len_len_key,
                byteorder='big'))

            package += len_key_package
            package += key_package

        package += bytearray(b'\x00') * (172 + 257 * (5 - count))

        return bytes(package)
