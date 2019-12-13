import unittest
from distributed_storage.client.settings import Settings


class Test_settings(unittest.TestCase):

    def test_len_len_value(self):
        settings = Settings(2048)

        result = settings.len_len_value

        self.assertEqual(2, result)

    def test_len_package(self):
        settings = Settings(2048)

        result = settings.len_package

        self.assertEqual(2308, result)


if __name__ == '__main__':
    unittest.main()
