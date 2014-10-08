# -*- coding: utf-8 -*-

from . import areas


class FailedRequest(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class Client(object):
    """
    The Podio API client. Callers should use the factory method OAuthClient to create instances.
    """

    def __init__(self, transport):
        self.transport = transport

    def __getattr__(self, name):
        new_trans = self.transport
        area = getattr(areas, name)
        return area(new_trans)

    def __dir__(self):
        """
        Should return list of attribute names.
        Since __getattr__ looks in areas, we simply list the content of the areas module
        """
        return dir(areas)
