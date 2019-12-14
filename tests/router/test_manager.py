import unittest
from unittest.mock import MagicMock
from distributed_storage.router.manager import Manager
import distributed_storage.router.manager as manager_modul


class Test_manager(unittest.TestCase):

    def test_connect(self):
        manager_modul.DSServer = MagicMock()
        manager = Manager(["123"], MagicMock(), MagicMock(), MagicMock(), 100)
        
        manager.connect(None, "123")

        self.assertTrue(manager_modul.DSServer.called)


if __name__ == '__main__':
    unittest.main()
