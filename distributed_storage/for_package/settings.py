import math
from decimal import Decimal


class Settings:

    def __init__(self):
        self._encoding = 'utf-8'

    @property
    def max_len_value(self):
        return 1200

    @property
    def encoding(self):
        return self._encoding

    @property
    def max_len_key(self):
        return 256

    @property
    def len_package(self):
        return 1460

    @property
    def len_len_value(self):
        return 2

    @property
    def len_len_key(self):
        return 1
