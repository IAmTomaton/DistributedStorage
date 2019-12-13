class Packer:

    def __init__(self, settings):
        self._settings = settings
        self._encoding = 'utf-8'

    def create_get_package(self, key):
        package = bytearray(b'g')

        key_byte = bytearray(key.encode(self._encoding))
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

        key_byte = bytearray(key.encode(self._encoding))
        len_key = len(key_byte)
        key_package = key_byte + bytearray(b'\x00') *\
            (self._settings.max_len_key - len_key)
        len_key_package = bytearray((len_key).to_bytes(
            self._settings.len_len_key,
            byteorder='big'))

        package += len_key_package
        package += key_package

        value_byte = bytearray(value.encode(self._encoding))
        len_value = len(value_byte)
        value_package = value_byte + bytearray(b'\x00') *\
            (self._settings.max_len_value - len_value)
        len_value_package = bytearray((len_value).to_bytes(
            self._settings.len_len_value,
            byteorder='big'))

        package += len_value_package
        package += value_package

        return bytes(package)
