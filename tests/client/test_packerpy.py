import unittest
from distributed_storage.client.packer import Packer
from distributed_storage.client.settings import Settings


class Test_packerpy(unittest.TestCase):

    def test_create_get_package(self):
        settings = Settings(2048)
        packer = Packer(settings)

        result = packer.create_get_package("testkey")

        self.assertEqual(2308, len(result))
        self.assertEqual(7, int.from_bytes(result[1:2], "big"))

    def test_create_set_package(self):
        settings = Settings(2048)
        packer = Packer(settings)

        result = packer.create_set_package("testkey", "value")
        
        self.assertEqual(2308, len(result))
        self.assertEqual(7, int.from_bytes(result[1:2], "big"))
        self.assertEqual(5, int.from_bytes(result[258:260], "big"))


if __name__ == '__main__':
    unittest.main()
