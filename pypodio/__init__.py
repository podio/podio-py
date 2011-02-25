from dolt import Dolt
'''
Module containing the PyPodio class and its associated helper
classes and methods
'''
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
        
    def authenticated(self):
        '''Checks whether the API object is authenticated'''

        if(self._token):
            if(self._token.expires_in > 0):
                return True
            else:
                self.refresh_oauth_token()
        return False

    def __call__(self, *args, **kwargs):
        self._attribute_stack += [str(a) for a in args]
        self._params = kwargs
        body = self._generate_body()
        if self._method == "POST":
            self._headers.update(
            {'content-type':'application/x-www-form-urlencoded'})
        if(self.authenticated() and ('authorization' not in self._headers)):
            self._headers.update(
                    {'authorization':"OAuth2 %s" % self._token.access_token}
                )
        if('url' not in kwargs):
            url = self.get_url()
        else:
            url = "%s%s" % (self._api_url, kwargs['url'])
        if('type' in kwargs):
            self._headers.update({'content-type': kwargs['type']})
        #print url
        response, data = self._http.request(
                url, 
                self._method,
                body=body,
                headers=self._headers)
        
        self._attribute_stack = []
        return self._handle_response(response, data)
    
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
            #print "Successfully Authenticated"
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
        if(type(app_id) == int):
            app_id = str(app_id)
        return self.POST(url = "/app/%s/activate" % app_id)
    
    def app_find(self, app_id):
        '''
        Finds application with id app_id.

          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        if(type(app_id) == int):
            app_id = str(app_id)
        return self.GET(url = "/app/%s" % app_id)