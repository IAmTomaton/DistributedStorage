import unittest
from distributed_storage.client.buffer import Buffer
from distributed_storage.packages.unpacker import Unpacker
from distributed_storage.packages.packer import Packer
from distributed_storage.packages.settings import Settings


class Test_test_buffer(unittest.TestCase):

    def test_handle_package(self):
        settings = Settings()
        unpacker = Unpacker(settings)
        packer = Packer(settings)
        buffer = Buffer(unpacker)
        package = packer.create_set_package("a", "qw")

        buffer.handle_package(package)

        self.assertEqual(("qw", None), buffer.get("a"))


if __name__ == '__main__':
    unittest.main()
