class Synchronizer:

    def __init__(self, settings):
        self._settings = settings

    def synchronize(self, synchronization_package):
        if synchronization_package[0] == b'y':
            settings._max_len_value = int(synchronization_package[1:4])
            return True
        return False
