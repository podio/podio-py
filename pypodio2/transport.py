# -*- coding: utf-8 -*-
from httplib2 import Http

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from .encode import multipart_encode


import json


class OAuthToken(object):
    """
    Class used to encapsulate the OAuthToken required to access the
    Podio API.

    Do not modify its attributes manually Use the methods in the
    Podio API Connector, get_oauth_token and refresh_oauth_token
    """
    def __init__(self, resp):
        self.expires_in = resp['expires_in']
        self.access_token = resp['access_token']
        self.refresh_token = resp['refresh_token']

    def to_headers(self):
        return {'authorization': "OAuth2 %s" % self.access_token}


class OAuthAuthorization(object):
    """Generates headers for Podio OAuth2 Authorization"""

    def __init__(self, login, password, key, secret, domain):
        body = {'grant_type': 'password',
                'client_id': key,
                'client_secret': secret,
                'username': login,
                'password': password}
        h = Http(disable_ssl_certificate_validation=True)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response, data = h.request(domain + "/oauth/token", "POST",
                                   urlencode(body), headers=headers)
        self.token = OAuthToken(_handle_response(response, data))

    def __call__(self):
        return self.token.to_headers()


class OAuthAppAuthorization(object):

    def __init__(self, app_id, app_token, key, secret, domain):
        body = {'grant_type': 'app',
                'client_id': key,
                'client_secret': secret,
                'app_id': app_id,
                'app_token': app_token}
        h = Http(disable_ssl_certificate_validation=True)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response, data = h.request(domain + "/oauth/token", "POST",
                                   urlencode(body), headers=headers)
        self.token = OAuthToken(_handle_response(response, data))

    def __call__(self):
        return self.token.to_headers()


class UserAgentHeaders(object):
    def __init__(self, base_headers_factory, user_agent):
        self.base_headers_factory = base_headers_factory
        self.user_agent = user_agent

    def __call__(self):
        headers = self.base_headers_factory()
        headers['User-Agent'] = self.user_agent
        return headers


class KeepAliveHeaders(object):

    def __init__(self, base_headers_factory):
        self.base_headers_factory = base_headers_factory

    def __call__(self):
        headers = self.base_headers_factory()
        headers['Connection'] = 'Keep-Alive'
        return headers


class TransportException(Exception):

    def __init__(self, status, content):
        super(TransportException, self).__init__()
        self.status = status
        self.content = content

    def __str__(self):
        return "TransportException(%s): %s" % (self.status, self.content)


class HttpTransport(object):
    def __init__(self, url, headers_factory):
        self._api_url = url
        self._headers_factory = headers_factory
        self._supported_methods = ("GET", "POST", "PUT", "HEAD", "DELETE",)
        self._attribute_stack = []
        self._method = "GET"
        self._posts = []
        self._http = Http(disable_ssl_certificate_validation=True)
        self._params = {}
        self._url_template = '%(domain)s/%(generated_url)s'
        self._stack_collapser = "/".join
        self._params_template = '?%s'

    def __call__(self, *args, **kwargs):
        self._attribute_stack += [str(a) for a in args]
        self._params = kwargs

        headers = self._headers_factory()

        if 'url' not in kwargs:
            url = self.get_url()
        else:
            url = self.get_url(kwargs['url'])

        if (self._method == "POST" or self._method == "PUT") and 'type' not in kwargs:
            headers.update({'content-type': 'application/json'})
            # Not sure if this will always work, but for validate/verfiy nothing else was working:
            body = json.dumps(kwargs)
        elif 'type' in kwargs:
            if kwargs['type'] == 'multipart/form-data':
                body, new_headers = multipart_encode(kwargs['body'])
                body = "".join(body)
                headers.update(new_headers)
            else:
                body = kwargs['body']
                headers.update({'content-type': kwargs['type']})
        else:
            body = self._generate_body()  # hack
        response, data = self._http.request(url, self._method, body=body, headers=headers)

        self._attribute_stack = []
        handler = kwargs.get('handler', _handle_response)
        return handler(response, data)

    def _generate_params(self, params):
        body = self._params_template % urlencode(params)
        if body is None:
            return ''
        return body

    def _generate_body(self):
        if self._method == 'POST':
            internal_params = self._params.copy()

            if 'GET' in internal_params:
                del internal_params['GET']

            return self._generate_params(internal_params)[1:]

    def _clear_content_type(self):
        """Clear content-type"""
        if 'content-type' in self._headers:
            del self._headers['content-type']

    def _clear_headers(self):
        """Clear all headers"""
        self._headers = {}

    def get_url(self, url=None):
        if url is None:
            url = self._url_template % {
                "domain": self._api_url,
                "generated_url": self._stack_collapser(self._attribute_stack),
            }
        else:
            url = self._url_template % {
                'domain': self._api_url,
                'generated_url': url[1:]
            }
            del self._params['url']

        if len(self._params):
            internal_params = self._params.copy()

            if 'handler' in internal_params:
                del internal_params['handler']

            if self._method == 'POST' or self._method == "PUT":
                if "GET" not in internal_params:
                    return url
                internal_params = internal_params['GET']
            url += self._generate_params(internal_params)
        return url

    def __getitem__(self, name):
        self._attribute_stack.append(name)
        return self

    def __getattr__(self, name):
        if name in self._supported_methods:
            self._method = name
        elif not name.endswith(')'):
            self._attribute_stack.append(name)
        return self


def _handle_response(response, data):
    if not data:
        data = '{}'
    else:
        data = data.decode("utf-8")
    if response.status >= 400:
        raise TransportException(response, data)
    return json.loads(data)
