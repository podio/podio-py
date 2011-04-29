import httplib2
import urllib
try:
    import json as simplejson
except ImportError:
    import simplejson

class OAuthToken(object):
    '''
    Class used to encapsulate the OAuthToken required to access the
    Podio API.

    Do not modify its attributes manually Use the methods in the
    Podio API Connector, get_oauth_token and refresh_oauth_token
    '''
    def __init__(self, resp):
        self.expires_in = resp['expires_in']
        self.access_token = resp['access_token']
        self.refresh_token = resp['refresh_token']
    
    def to_headers(self):
        return {'authorization':"OAuth2 %s" % self.access_token}


class OAuthAuthorization(object):
    """
    Generates headers for Podio OAuth2 Authorization"
    """
    def __init__(self, login, password, key, secret, domain):
        body = {'grant_type':'password',
                'client_id':key,
                'client_secret':secret,
                'username':login,
                'password':password}
        h = httplib2.Http()
        headers = {'content-type':'application/x-www-form-urlencoded'}
        resp, content = h.request(domain + "/oauth/token", "POST",
                                  urllib.urlencode(body), headers=headers)
        if resp['status'] == '200':
             self.token = OAuthToken(simplejson.loads(content)).to_headers()
    def __call__(self):
        return self.token

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
        self.status = status
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "TransportException(%r)" % (self.status)


class HttpTransport(object):
    def __init__(self, url, headers_factory):
        self._api_url = url
        self.headers = headers_factory()
        self._supported_methods = ("GET", "POST", "PUT", "HEAD", "DELETE",)
        self._attribute_stack = []
        self._method = "GET"
        self._posts = []
        self._http = httplib2.Http()
        self._params = {}
        self._url_template = '%(domain)s/%(generated_url)s'
        self._stack_collapser = "/".join
        self._params_template = '?%s'

    def __call__(self, *args, **kwargs):
        self._attribute_stack += [str(a) for a in args]
        self._params = kwargs
        if self._method == "POST" and 'type' not in kwargs:
            self.headers.update(
            {'content-type':'application/x-www-form-urlencoded'})
            body = self._generate_body()
        elif('type' in kwargs):
            body = kwargs['body']
            self._headers.update({'content-type': kwargs['type']})
        else:
            body = self._generate_body() #hack
        if('url' not in kwargs):
            url = self.get_url()
        else:
            url = self.get_url(kwargs['url'])
        response, data = self._http.request(url, self._method, body=body, headers=self.headers)
        self._attribute_stack = []
        return self._handle_response(response, data)
    
    def _generate_params(self, params):
        body = self._params_template % urllib.urlencode(params)
        if body is None:
            return ''
        return body

    def _generate_body(self):
        if self._method == 'POST':
            internal_params = self._params.copy()
            if 'GET' in internal_params:
                del internal_params['GET']
            return self._generate_params(internal_params)[1:]

    def _handle_response(self, response, data):
        if response.status >= 400:
            raise TransportException(response, data)
        return simplejson.loads(data)

    def __getitem__(self, name):
        self._attribute_stack.append(name)
        return self

    def __getattr__(self, name):
        if name in self._supported_methods:
            self._method = name
        elif not name.endswith(')'):
            self._attribute_stack.append(name)
        return self
    
    def _clear_headers(self):
        '''Clear content-type'''
        if 'content-type' in self._headers:
            del self._headers['content-type']

    def get_url(self, url=None):
        if not url:
            url = self._url_template % {
                "domain": self._api_url,
                "generated_url" : self._stack_collapser(self._attribute_stack),
            }
        else:
            url = self._url_template % {
                'domain': self._api_url,
                'generated_url': url[1:]
            }   
            del self._params['url']      
        if len(self._params):
            internal_params = self._params.copy()
            if self._method == 'POST':
                if "GET" not in internal_params:
                    return url
                internal_params = internal_params['GET']
            url += self._generate_params(internal_params)
        return url