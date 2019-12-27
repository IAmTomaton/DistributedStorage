import unittest
from distributed_storage.packages.packer import Packer
from distributed_storage.packages.settings import Settings


class Test_packer(unittest.TestCase):

    def test_create_get_package(self):
        settings = Settings()
        packer = Packer(settings)

        result = packer.create_get_package("testkey")

        self.assertEqual(1284, len(result))
        self.assertEqual(7, int.from_bytes(result[1:2], "big"))

    def test_create_set_package(self):
        settings = Settings()
        packer = Packer(settings)

        result = packer.create_set_package("testkey", "value")
        
        self.assertEqual(1284, len(result))
        self.assertEqual(7, int.from_bytes(result[1:2], "big"))
        self.assertEqual(5, int.from_bytes(result[258:260], "big"))

    def test_create_sync_package(self):
        settings = Settings()
        packer = Packer(settings)

        result = packer.create_sync_package()
        
        self.assertEqual(1284, len(result))
        self.assertEqual(1024, int.from_bytes(result[1:5], "big"))

    def test_create_error_package(self):
        settings = Settings()
        packer = Packer(settings)

        result = packer.create_error_package("1", "2")
        
        self.assertEqual(1284, len(result))


if __name__ == '__main__':
    unittest.main()
