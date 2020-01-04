import unittest
from distributed_storage.server.data import Data
from distributed_storage.for_package.packer import Packer
from distributed_storage.for_package.unpacker import Unpacker
from distributed_storage.for_package.settings import Settings


class Test_test_data(unittest.TestCase):

    def test_simple(self):
        settings = Settings()

        unpacker = Unpacker(settings)
        packer = Packer(settings)
        data = Data(packer, unpacker, settings, 0, path="test_data")

        data._set_value("dsf", "saf")

        result = data._get_value("dsf")

        self.assertEqual("saf", result)

        data.clear()

    def test_double_key(self):
        settings = Settings()

        unpacker = Unpacker(settings)
        packer = Packer(settings)
        data = Data(packer, unpacker, settings, 0, path="test_data")

        data._set_value("dsf", "saf")
        data._set_value("dsf2", "saf2")

        result = data._get_value("dsf2")

        self.assertEqual("saf2", result)

        data.clear()

    def test_rewrite_key(self):
        settings = Settings()

        unpacker = Unpacker(settings)
        packer = Packer(settings)
        data = Data(packer, unpacker, settings, 0, path="test_data")

        data._set_value("dsf", "saf")
        data._set_value("dsf", "s2")

        result = data._get_value("dsf")

        self.assertEqual("s2", result)

        data.clear()


if __name__ == '__main__':
    unittest.main()
