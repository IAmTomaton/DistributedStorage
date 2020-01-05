import unittest
from distributed_storage import Client
from distributed_storage import LenKeyException
from distributed_storage import LenValueException


class Test_test_client(unittest.TestCase):

    def test_len_key(self):
        try:
            client = Client("localhost", 9090)
            client.start()

            with self.assertRaises(LenKeyException):
                client.set("1" * 251, "456")

        finally:
            client.turn_off()

    def test_len_value(self):
        try:
            client = Client("localhost", 9090)
            client.start()

            with self.assertRaises(LenValueException):
                client.set("1", "4" * 1201)

        finally:
            client.turn_off()


if __name__ == '__main__':
    unittest.main()
