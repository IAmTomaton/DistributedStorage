from distributed_storage.router.manager import Manager
from distributed_storage.router.server_connector import ServerConnector
from distributed_storage.router.client_connector import ClientConnector
from distributed_storage.packages import Packer
from distributed_storage.packages import Settings
from distributed_storage.packages import Unpacker


class Router:

    def __init__(self, server_ip, server_port, client_ip, client_port,
                 number_servers):
        settings = Settings()
        settings.max_len_value = 2048
        packer = Packer(settings)
        unpacker = Unpacker(settings)
        manager = Manager(packer, unpacker, settings, number_servers)
        server_connector = ServerConnector(server_ip, server_port, manager,
                                           settings, packer, unpacker)
        server_connector.start()
        client_connector = ClientConnector(client_ip, client_port, manager,
                                           unpacker)
        client_connector.start()
