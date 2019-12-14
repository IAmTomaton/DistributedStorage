import unittest
from distributed_storage.client.ds_client import DSClient
from distributed_storage.exeptions.connect_exeption import ConnectExeption
import time


class Test_ds_client(unittest.TestCase):

    def test_work_connect_exeption(self):
        ds_client = DSClient("localhost", 9090, None, None)
        self.assertRaises(ConnectExeption, ds_client._work)


if __name__ == '__main__':
    unittest.main()