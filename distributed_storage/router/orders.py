from threading import Lock


class Orders:

    def __init__(self):
        self._lock = Lock()
        self._orders = []

    def add_order(self, order):
        self._lock.acquire()
        try:
            self._orders.append(order)
            order.add_count()
        finally:
            self._lock.release()

    def send(self, command, key, package, number, packer, manager):
        self._lock.acquire()
        try:
            index = 0
            while index < len(self._orders):
                order = self._orders[index]
                if order.send(command, key, package, number):
                    self._orders.pop(index)
                    self._check_order(order, packer, manager)
                else:
                    index += 1
        finally:
            self._lock.release()

    def _check_order(self, order, packer, manager):
        if order.count == 0:
            if order.package is None:
                order.customer.send(packer.create_error_package_not_key(order.key))
            else:
                errors = order.errors
                for i in errors:
                    manager.try_send_set_package(i, order.key, order.package)

    def skip(self):
        for order in self._orders:
            order.skip()
        self._orders = []
