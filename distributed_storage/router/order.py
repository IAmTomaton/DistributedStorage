class Order:

    def __init__(self, key, customer):
        self._customer = customer
        self._key = key
        self._completed = False

    def send(self, package):
        self._customer.send(package)

    def check_key(self, key):
        return key == self._key
