class DSException(Exception):

    def __init__(self):
        self._value = "DSException"

    def __str__(self):
        return(repr(self._value))


class NoKeyException(DSException):

    def __init__(self, key):
        self._value = "this key is not in storage: " + key

    def __str__(self):
        return(repr(self._value))


class NoServerException(DSException):

    def __init__(self, key):
        self._value = "there are no servers that could store this key: " +\
            key

    def __str__(self):
        return(repr(self._value))


class NoRouterException(DSException):

    def __init__(self):
        self._value = "the client is not connected to the router"

    def __str__(self):
        return(repr(self._value))


class LenKeyException(DSException):

    def __init__(self, key):
        self._value = "the key length should be no more than 250, " +\
            "you had {}".format(len(key))

    def __str__(self):
        return(repr(self._value))


class LenValueException(DSException):

    def __init__(self, value):
        self._value = "the value length should be no more than 1200, " +\
            "you had {}".format(len(value))

    def __str__(self):
        return(repr(self._value))
