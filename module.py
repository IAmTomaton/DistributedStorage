from distributed_storage import Router
import socket
from time import sleep
from distributed_storage.client.client import Client
from distributed_storage.server.server import Server


router = Router("", 9091, "", 9090, 5)

router.start()

server = Server("localhost", 9091, 0)
server.start()

#client = Client("localhost", 9090)
#client.start()

#value, error = client.get("123")
#print(value)
#print(error)

sleep(3)

server.turn_off()
#client.turn_off()
router.turn_off()
