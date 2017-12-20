import weakref

class APIEndpoint(object):
    def __init__(self, parent):
        self._api = weakref.ref(parent)