from distributed_storage.router.manager import Manager
from distributed_storage.router.ds_router import DSRouter
from distributed_storage.packages import Packer
from distributed_storage.packages import Settings
from distributed_storage.packages import Unpacker


class Router:

    def __init__(self, ip, port, server_addresses):
        settings = Settings()
        packer = Packer(settings)
        unpacker = Unpacker(settings)
        manager = Manager(server_addresses, packer, unpacker, settings, 2048)
        ds_router = DSRouter(ip, port, manager)
        ds_router.start()
