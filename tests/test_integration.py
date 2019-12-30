import unittest
from distributed_storage import Router
from time import sleep
from distributed_storage import Client
from distributed_storage import Server


SERVER_PORT = 9091
CLIENT_PORT = 9090


class Test_test_integration(unittest.TestCase):

    def test_simple(self):
        try:
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server = Server("localhost", SERVER_PORT, 3)
            server.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            client.set("123", "456")

            # value, error = client.get("123")

            # self.assertEqual("456", value)
            # self.assertIsNone(error)

        finally:
            server.turn_off()
            client.turn_off()
            router.turn_off()
            sleep(0.2)

    def test_early_correction(self):
        try:
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server0 = Server("localhost", SERVER_PORT, 3)
            server0.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            client.set("123", "456")

            server1 = Server("localhost", SERVER_PORT, 4)
            server1.start()

            sleep(0.2)

            server0.turn_off()

            sleep(0.2)

            # value, error = client.get("123")

            # self.assertEqual("456", value)
            # self.assertIsNone(error)

        finally:
            server1.turn_off()
            client.turn_off()
            router.turn_off()
            sleep(0.2)

    def test_late_correction(self):
        try:
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server0 = Server("localhost", SERVER_PORT, 3)
            server0.start()

            server1 = Server("localhost", SERVER_PORT, 4)
            server1.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            client.set("123", "456")

            sleep(0.2)

            server1._data._data = {}

            client.get("123")

            sleep(0.2)

            server0.turn_off()

            sleep(0.2)

            # value, error = client.get("123")

            # self.assertEqual("456", value)
            # self.assertIsNone(error)

        finally:
            server1.turn_off()
            client.turn_off()
            router.turn_off()
            sleep(0.2)

    def test_reconnect_server(self):
        try:
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server = Server("localhost", SERVER_PORT, 3)
            server.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            client.set("123", "456")

            sleep(0.2)

            server.turn_off()

            sleep(0.2)

            server.start()

            sleep(0.2)

            # value, error = client.get("123")

            # self.assertIsNone(error)
            # self.assertEqual("456", value)

        finally:
            server.turn_off()
            client.turn_off()
            router.turn_off()
            sleep(0.2)

    def test_reconnect_router(self):
        try:
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server = Server("localhost", SERVER_PORT, 3)
            server.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            client.set("123", "456")

            sleep(0.2)

            router.turn_off()

            sleep(1)

            router.start()

            sleep(1)

            # value, error = client.get("123")

            # self.assertIsNone(error)
            # self.assertEqual("456", value)

        finally:
            server.turn_off()
            client.turn_off()
            router.turn_off()
            sleep(0.2)

    def test_reconnect_client(self):
        try:
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server = Server("localhost", SERVER_PORT, 3)
            server.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            client.set("123", "456")

            sleep(0.2)

            client.turn_off()

            sleep(0.2)

            client.start()

            sleep(0.2)

            # value, error = client.get("123")

            # self.assertIsNone(error)
            # self.assertEqual("456", value)

        finally:
            server.turn_off()
            client.turn_off()
            router.turn_off()
            sleep(0.2)


if __name__ == '__main__':
   # unittest.main()
   pass
