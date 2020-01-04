from distributed_storage.for_package.unpacker import Unpacker
from distributed_storage.for_package.packer import Packer
from distributed_storage.for_package.settings import Settings
import unittest


class Test_unpacker(unittest.TestCase):

    def test_set(self):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)

        package = packer.create_set_package("key", "as")

        command, key, value = unpacker.parse_package(package)

        self.assertEqual("s", command)
        self.assertEqual("key", key)
        self.assertEqual("as", value)

    def test_get(self):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)

        package = packer.create_get_package("key")

        command, key, value = unpacker.parse_package(package)

        self.assertEqual("g", command)
        self.assertEqual("key", key)
        self.assertEqual("", value)

    def test_number(self):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)

        package = packer.create_number_package(10)

        result = unpacker.parse_number_package(package)

        self.assertEqual(10, result)

    def test_get_keys(self):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)

        package = packer.create_get_keys_package(10)

        result = unpacker.parse_get_keys_package(package)

        self.assertEqual(10, result)

    def test_count_keys(self):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)

        package = packer.create_count_keys_package(10, 13)

        result = unpacker.parse_count_keys_package(package)

        self.assertEqual((10, 13), result)

    def test_count_keys(self):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)

        package = packer.create_keys_package(10, ["123", "456"])

        result = unpacker.parse_keys_package(package)

        self.assertEqual((10, ["123", "456"]), result)


if __name__ == '__main__':
    unittest.main()
