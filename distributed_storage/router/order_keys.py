from distributed_storage.for_package.unpacker import Unpacker


class OrderKeys:

    def __init__(self, number, customer, unpacker, count_servers):
        self._customer = customer
        self._number_data = number
        self._unpacker = unpacker
        self._counts = [0 for i in range(count_servers)]

    def add_count(self):
        pass

    @property
    def count(self):
        return 1

    @property
    def customer(self):
        return self._customer

    def send(self, command, key, package, number):
        unpaker = self._unpacker
        number_data = unpaker.parse_number_data(package)
        if number_data == self._number_data:
            if command == 'c':
                number_data, count = unpaker.parse_count_keys_package(package)
                self._counts[number] += count
                return self._counts[number] == 0
            elif command == 'k':
                number_data, keys = unpaker.parse_keys_package(package)
                self._counts[number] -= len(keys)
                self._customer.send(package)
                return self._counts[number] == 0
        return False

    def skip(self):
        pass
