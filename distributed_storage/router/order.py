class Order:

    def __init__(self, key, customer):
        self._customer = customer
        self._key = key
        self._errors = []
        self._package = None
        self._count = 0

    def add_count(self):
        self._count += 1

    @property
    def count(self):
        return self._count

    @property
    def errors(self):
        return self._errors

    @property
    def customer(self):
        return self._customer

    @property
    def package(self):
        return self._package

    @property
    def key(self):
        return self._key

    def send(self, command, key, package, number):
        if not self._check_key(key):
            return False

        self._count -= 1
        if command == "s" and self._package is None:
            self._customer.send(package)
            self._package = package
        elif command == "e":
            self._errors.append(number)

        return True

    def _check_key(self, key):
        return key == self._key

    def skip(self):
        self._count -= 1
