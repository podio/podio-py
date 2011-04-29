from pypodio2 import areas

class FailedRequest(Exception):
    def __init__(self, error):
        self.error = error
    def __str__(self):
        return repr(self.error)

class Client(object):
    """The Podio API client. Callers should use the factory
    method OAuthClient to create instances.
    """        
    def __init__(self, transport):
        self.transport = transport

    def __getattr__(self, name):
        area = getattr(areas, name)
        return area(self.transport)