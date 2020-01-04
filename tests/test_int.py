import unittest
from distributed_storage import Router
from time import sleep
from distributed_storage import Client
from distributed_storage import Server


SERVER_PORT = 9091
CLIENT_PORT = 9090


class Test_test_int(unittest.TestCase):

    def test_simple(self):
        try:
            sleep(0.2)

            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server = Server("localhost", SERVER_PORT, 3, "data")
            server.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            sleep(0.2)

            client.set("123", "456")
            client.send_get("123")

            sleep(0.2)

            value, error = client.get("123")

            self.assertEqual("456", value)
            self.assertIsNone(error)

        finally:
            server.turn_off()
            server.clear()
            client.turn_off()
            router.turn_off()

if __name__ == '__main__':
    unittest.main()
