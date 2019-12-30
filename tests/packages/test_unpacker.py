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


if __name__ == '__main__':
    unittest.main()
