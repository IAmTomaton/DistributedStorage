import unittest
from distributed_storage import Router
from time import sleep
from distributed_storage import Client
from distributed_storage import Server
from distributed_storage import NoRouterException
import socket


SERVER_PORT = 9091
CLIENT_PORT = 9090


class Test_test_integration(unittest.TestCase):

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

    def test_early_correction(self):
        try:
            sleep(0.2)
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server0 = Server("localhost", SERVER_PORT, 3, "data")
            server0.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            sleep(0.2)

            client.set("123", "456")

            sleep(0.2)

            server1 = Server("localhost", SERVER_PORT, 4, "data")
            server1.start()

            sleep(0.2)

            server0.turn_off()

            sleep(0.2)

            client.send_get("123")

            sleep(0.2)

            value, error = client.get("123")

            self.assertEqual("456", value)
            self.assertIsNone(error)

        finally:
            server1.turn_off()
            server1.clear()
            server0.clear()
            client.turn_off()
            router.turn_off()

    def test_late_correction(self):
        try:
            sleep(0.2)
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            server0 = Server("localhost", SERVER_PORT, 3, "data")
            server0.start()

            server1 = Server("localhost", SERVER_PORT, 4, "data")
            server1.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            sleep(0.2)

            client.set("123", "456")

            sleep(0.2)

            server1._data._data = {}

            client.send_get("123")

            sleep(0.2)

            client.get("123")

            server0.turn_off()

            sleep(0.2)

            client.send_get("123")

            sleep(0.2)

            value, error = client.get("123")

            self.assertEqual("456", value)
            self.assertIsNone(error)

        finally:
            server1.turn_off()
            server1.clear()
            server0.clear()
            client.turn_off()
            router.turn_off()

    def test_reconnect_server(self):
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

            sleep(0.2)

            server.turn_off()

            sleep(0.2)

            server.start()

            sleep(0.2)

            client.send_get("123")

            sleep(0.2)

            value, error = client.get("123")

            self.assertIsNone(error)
            self.assertEqual("456", value)

        finally:
            server.turn_off()
            server.clear()
            client.turn_off()
            router.turn_off()

    def test_reconnect_router(self):
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

            sleep(0.2)
            
            router.turn_off()

            sleep(0.2)

            router.start()

            sleep(0.4)

            client.send_get("123")

            sleep(0.2)

            value, error = client.get("123")

            self.assertIsNone(error)
            self.assertEqual("456", value)

        finally:
            server.turn_off()
            server.clear()
            client.turn_off()
            router.turn_off()

    def test_reconnect_client(self):
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

            sleep(0.2)

            client.turn_off()

            sleep(0.2)

            client.start()

            sleep(0.2)

            client.send_get("123")

            sleep(0.2)

            value, error = client.get("123")

            self.assertIsNone(error)
            self.assertEqual("456", value)

        finally:
            server.turn_off()
            server.clear()
            client.turn_off()
            router.turn_off()

    def test_router_not_connect(self):
        try:
            sleep(0.2)
            client = Client("localhost", CLIENT_PORT)
            client.start()

            with self.assertRaises(NoRouterException):
                client.set("123", "456")

        finally:
            client.turn_off()
            sleep(0.2)

    def test_router_buffer(self):
        try:
            sleep(0.2)
            router = Router("", SERVER_PORT, "", CLIENT_PORT, 5)
            router.start()

            client = Client("localhost", CLIENT_PORT)
            client.start()

            sleep(0.2)

            client.set("123", "456")

            sleep(0.2)

            server = Server("localhost", SERVER_PORT, 3, "data")
            server.start()

            sleep(0.2)

            client.send_get("123")

            sleep(0.2)

            value, error = client.get("123")

            self.assertIsNone(error)
            self.assertEqual("456", value)

        finally:
            server.turn_off()
            server.clear()
            client.turn_off()
            router.turn_off()


if __name__ == '__main__':
    unittest.main()
