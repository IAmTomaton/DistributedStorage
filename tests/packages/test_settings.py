import unittest
from distributed_storage.for_package.settings import Settings


class Test_settings(unittest.TestCase):

    def test_len_len_value(self):
        settings = Settings()

        result = settings.len_len_value

        self.assertEqual(2, result)

    def test_len_package(self):
        settings = Settings()

        result = settings.len_package

        self.assertEqual(1460, result)


if __name__ == '__main__':
    unittest.main()
