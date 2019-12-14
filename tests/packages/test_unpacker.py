from distributed_storage.packages.unpacker import Unpacker
from distributed_storage.packages.packer import Packer
from distributed_storage.packages.settings import Settings
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

    def test_sync(self):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)

        package = packer.create_sync_package(1000)

        command, key, value = unpacker.parse_package(package)

        self.assertEqual(1000, settings.max_len_value)
        self.assertEqual(None, command)
        self.assertEqual(None, key)
        self.assertEqual(None, value)


if __name__ == '__main__':
    unittest.main()
