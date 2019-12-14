import unittest
from distributed_storage.packages.packer import Packer
from distributed_storage.packages.settings import Settings


class Test_packer(unittest.TestCase):

    def test_create_get_package(self):
        settings = Settings()
        packer = Packer(settings)

        result = packer.create_get_package("testkey")

        self.assertEqual(2308, len(result))
        self.assertEqual(7, int.from_bytes(result[1:2], "big"))

    def test_create_set_package(self):
        settings = Settings()
        packer = Packer(settings)

        result = packer.create_set_package("testkey", "value")
        
        self.assertEqual(2308, len(result))
        self.assertEqual(7, int.from_bytes(result[1:2], "big"))
        self.assertEqual(5, int.from_bytes(result[258:260], "big"))

    def test_create_sync_package(self):
        settings = Settings()
        packer = Packer(settings)

        result = packer.create_sync_package(100)
        
        self.assertEqual(2308, len(result))
        self.assertEqual(100, int.from_bytes(result[1:5], "big"))


if __name__ == '__main__':
    unittest.main()
