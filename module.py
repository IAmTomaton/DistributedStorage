from distributed_storage import Router
from time import sleep
from distributed_storage.client.client import Client
from distributed_storage.server.server import Server


try:
    router = Router("", 9095, "", 9097, 5)
    router.start()

    server = Server("localhost", 9095, 0)
    server.start()

    client = Client("localhost", 9090)
    client.start()

    sleep(1)

    client.set("123", "456")

    value, error = client.get("123")
    print(value)
    print(error)

finally:
    sleep(1)
    server.turn_off()
    client.turn_off()
    router.turn_off()
