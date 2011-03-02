'''
Module containing the PyPodio class and its associated helper
classes and methods
'''

from dolt import Dolt
import urllib
import httplib2
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

class ApiErrorException(Exception):
    '''Base class for errors from the API'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Podio(Dolt):
    '''
    A Python interface to the Podio API.

    Currently the API does not cache any requests.

    Sample Usage:
      The API expects to be passed a client_id and client_secret when
      it is instantiated:
        
        >>> import pypodio
        >>> api = pypodio.Podio(client_id = id, client_secret = secret)
    
    Once instantiated, you need to request an OAuth Token and get
    authorization to operate as a user:
        >>> api.request_oauth_token(username, password)

    If it is successful then a result of True will be returned, and a call
    to api.authenticated() will also.  
    '''
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super(Podio, self).__init__(*args, **kwargs)
        self._api_url = "https://api.podio.com"
        self._url_template = "%(domain)s/%(generated_url)s"
        self._headers = {}
        self._token = None
        if(client_id and client_secret):
            self._client_id = client_id
            self._client_secret = client_secret
        else:
            raise NotImplementedError
    
    def _clear_headers(self):
        '''Clear content-type'''
        if 'content-type' in self._headers:
            del self._headers['content-type']
    
    def get_url(self, url=None, endpoint=None):
        if not url:
            url = self._url_template % {
                "domain": self._api_url,
                "generated_url" : self._stack_collapser(self._attribute_stack),
            }
        else:
            if endpoint:
                url = self._url_template % {
                    'domain': endpoint,
                    'generated_url': url[1:]
                }
                del self._params['endpoint']
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
    
    def _handle_response(self, response, data):
        try:
            return simplejson.loads(data)
        except ValueError:
            return data

    def __call__(self, *args, **kwargs):
        self._attribute_stack += [str(a) for a in args]
        self._params = kwargs
        
        if self._method == "POST" and 'type' not in kwargs:
            self._headers.update(
            {'content-type':'application/x-www-form-urlencoded'})
            body = self._generate_body()
        elif('type' in kwargs):
            body = kwargs['body']
            self._headers.update({'content-type': kwargs['type']})
        else:
            body = self._generate_body() #hack
                
        if(self.authenticated() and ('authorization' not in self._headers)):
            self._headers.update({'authorization':"OAuth2 %s" %
            (self._token.access_token)})

        if('url' not in kwargs):
            url = self.get_url()
        else:
            if 'endpoint' in kwargs:
                url = self.get_url(kwargs['url'], kwargs['endpoint'])
            else:
                url = self.get_url(kwargs['url'])
        response, data = self._http.request(
                url, 
                self._method,
                body=body,
                headers=self._headers)
        self._clear_headers()
        self._attribute_stack = []
        return self._handle_response(response, data)
    
    def _sanitize_id(self, item_id):
        '''Sanitize id if passed as int'''
        if(type(item_id) == int):
            return str(item_id)
        return item_id

    def authenticated(self):
        '''Checks whether the API object is authenticated'''

        if(self._token):
            if(self._token.expires_in > 0):
                return True
            else:
                self.refresh_oauth_token()
        return False

        
    #Start implementation of "OAuth" area API calls

    def request_oauth_token(self, username, password):
        '''
        Call with a username and password to fetch an API OAuth token.

          Arguments:
            username: String representation of username/email
            password: Corresponding password                     
        returns
          A Boolean describing if the operation succeeded or failed
        '''

        resp = self.POST.oauth.token(grant_type="password", 
            client_id=self._client_id,
            client_secret=self._client_secret,
            username=username, 
            password=password)
        if('access_token' in resp):
            self._token = OAuthToken(resp)
            self._headers.update(
                    {'authorization':"OAuth2 %s" % self._token.access_token}
                )
            return True
        else:
            raise ApiErrorException(resp)
    def _refresh_oauth_token(self):
        '''
        Refreshes the API instance's OAuth token. For internal use only.
        '''
        self.POST.oauth.token(
            grant_type="refresh_token",
            client_id=self._client_id, 
            client_secret=self._client_secret, 
            refresh_token = self._token.refresh_token
        )
    
    #Start implementation of "Users" area API calls 

    def users_get_active_profile(self):
        '''
        Returns the profile of the currently logged in user
        as a Python dictionary.
        '''
        return self.GET(url="/user/profile/")
    
    #Start implementation of "Applications" area API calls

    def app_activate_app(self, app_id):
        '''
        Activates the application with app_id
          
          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        app_id = self._sanitize_id(app_id)
        return self.POST(url = "/app/%s/activate" % app_id)
    
    def app_find(self, app_id):
        '''
        Finds application with id app_id.

          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        app_id = self._sanitize_id(app_id)
        return self.GET(url = "/app/%s" % app_id)
    
    def app_list_apps_in_space(self, space_id):
        '''
        Returns a list of all the visible apps in a space.

          Arguemtns:
            space_id: Space ID as a string
        '''
        space_id = self._sanitize_id(space_id)
        return self.GET(url = "/app/space/%s/" % space_id)

    def app_get_items(self, app_id, **kwargs):
        app_id = self._sanitize_id(app_id)
        return self.GET(url = "/item/app/%s/" % app_id, **kwargs)

    def space_find_by_url(self, space_url, id_only=True):
        '''
        Returns a space ID given the URL of the space.

          Arguments:
            space_url: URL of the Space
          
          Returns:
            space_id: Space url as string
        '''        
        resp = self.GET(url = "/space/url?%s" % urllib.urlencode(dict(url=space_url)))
        if id_only:
            return resp['space_id']
        return resp
    
    def space_find_all_for_org(self, org_id):
        '''
        Find all of the spaces in a given org.
          
          Arguments:
            org_id: Orginization ID as string
          returns:
            Dict containing details of spaces
        '''
        org_id = self._sanitize_id(org_id)
        return self.GET(url = "/org/%s/space/" % org_id)
    
    def space_create(self, attributes):
        '''
        Create a new space
          
          Arguments:
            Refer to API. Pass in argument as dictionary
          returns:
            Dict containing details of newly created space
        '''
        if type(attributes) != dict:
            raise ApiErrorException("Dictionary of values expected")
        attributes = json.dumps(attributes)
        return self.POST(
            url = "/space/", 
            body = attributes, 
            type = 'application/json'
        )
    
    #Start Item operation implementations

    def items_get_item(self, item_id, basic=False, **kwargs):
        '''Get item

          Arguments:
            item_id: Item's id
          Returns:
            Dict with item info
        '''
        item_id = self._sanitize_id(item_id)
        if basic:
            return self.GET(url = "/item/%s/basic" % item_id)
        return self.GET(kwargs, url = "/item/%s" % item_id)

    def items_next_item(self, item_id, **kwargs):
        item_id = self._sanitize_id(item_id)
        return self.GET(url = "/item/%s/next" % item_id)
    
    def items_prev_item(self, item_id, **kwargs):
        item_id = self._sanitize_id(item_id)
        return self.GET(url = "/item/%s/previous" % item_id)
    
    #Start File Implementations

    def files_get_file(self, file_id, size=None, return_url=True):
        '''
        Get a file's URL
        '''
        file_id = self._sanitize_id(file_id)
        endpoint = "https://download.podio.com"
        if size:
            url = "%s/%s" % (file_id, size)
        else:
            url = "/%s" % (file_id)
        if return_url:
            return endpoint+url
        else:
            return self.GET(endpoint=endpoint, url=url)