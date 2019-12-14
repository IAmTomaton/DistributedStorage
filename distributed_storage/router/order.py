class Order:

    def __init__(self, key, customer):
        self._customer = customer
        self._key = key
        self._completed = False

    def send(self, key, package):
        if self._check_key(key):
            self._customer.send(package)
            self._completed = True

    @property
    def is_completed(self):
        return self._completed

    def _check_key(self, key):
        return key == self._key
