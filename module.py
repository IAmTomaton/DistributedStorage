from distributed_storage import Router
from time import sleep
from distributed_storage.client.client import Client
from distributed_storage.server.server import Server


try:
    router = Router("", 9091, "", 9090, 5)
    router.start()

    server0 = Server("localhost", 9091, 0)
    server0.start()

    client = Client("localhost", 9090)
    client.start()

    sleep(1)

    client.set("123", "456")

    router._manager._application_table[2] = []

    sleep(1)

    server2 = Server("localhost", 9091, 2)
    server2.start()

    value, error = client.get("123")
    print(value)
    print(error)

    sleep(1)


finally:
    server0.turn_off()
    server2.turn_off()
    client.turn_off()
    router.turn_off()
