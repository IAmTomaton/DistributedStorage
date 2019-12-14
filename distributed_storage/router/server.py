from multiprocessing import Queue


class Server:

    def __init__(self):
        self.ds_server = None
        self._applications = Queue()

    @property
    def applications(self):
        return self._applications

    def add_order(self, order):
        self.ds_server.add_order(order)

    @property
    def is_connected(self):
        return self.ds_server is not None
