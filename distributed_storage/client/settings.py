import math


class Settings:

    def __init__(self, max_len_value):
        self._max_len_value = max_len_value
        self._max_len_key = 256

    @property
    def max_len_value(self):
        return self._max_len_value

    @property
    def max_len_key(self):
        return self._max_len_key

    @property
    def len_package(self):
        return 1 + 1 + 256 + self.len_len_value + self.max_len_value

    @property
    def len_len_value(self):
        return math.ceil(math.log(self.max_len_value, 256))

    @property
    def len_len_key(self):
        return math.ceil(math.log(self.max_len_key, 256))
