class NoKeyException(Exception):

    def __init__(self, key):
        self._value = "this key is not in storage" + key

    def __str__(self):
        return(repr(self._value))


class NoServerException(Exception):

    def __init__(self, key):
        self._value = "there are no servers that could store this key" + key

    def __str__(self):
        return(repr(self._value))


class NoRouterException(Exception):

    def __init__(self):
        self._value = "the client is not connected to the router"

    def __str__(self):
        return(repr(self._value))
