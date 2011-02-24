from dolt import Dolt

class OAuthToken(object):
	def __init__(self, resp):
		self.expires_in = resp['expires_in']
		self.access_token = resp['access_token']
		self.refresh_token = resp['refresh_token']

class ApiErrorException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class Podio(Dolt):
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
		if(self._token):
			if(self._token.expires_in > 0):
				return True
			else:
				refresh_access_token()
		return False

	def __call__(self, *args, **kwargs):
		self._attribute_stack += [str(a) for a in args]
		self._params = kwargs
		body = self._generate_body()
		if self._method == "POST":
			self._headers.update({'content-type':'application/x-www-form-urlencoded'})
		if(self.authenticated() and ('authorization' not in self._headers)):
			self._headers.update({'authorization':"OAuth2 %s" % self._token.access_token})
		#print self._headers
		if('url' not in kwargs):
			url = self.get_url()
		else:
			url = "%s%s" % (self._api_url, kwargs['url'])
		if('type' in kwargs):
			self._headers.update({'content-type': kwargs['type']})
		#print url
		response, data = self._http.request(url, self._method, body=body, headers=self._headers)
		
		self._attribute_stack = []
		return self._handle_response(response, data)
	
	#Start implementation of "OAuth" area API calls

	def request_oauth_token(self, username, password):
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
	def refresh_access_token(self):
		resp = self.POST.oauth.token(
			grant_type="refresh_token",
			client_id=self._client_id, 
			client_secret=self._client_secret, 
			refresh_token = self._token.refresh_token
		)
	
	#Start implementation of "Users" area API calls 

	def users_get_active_profile(self):
		return self.GET(url="/user/profile/")
	
	#Start implementation of "Applications" area API calls

	def app_activate_app(self, app_id):
		if(type(app_id) == int):
			app_id = str(app_id)
		return self.POST(url = "/app/%s/activate" % app_id)
	
	def app_find(self, app_id):
		if(type(app_id) == int):
			app_id = str(app_id)
		return self.GET(url = "/app/%s" % app_id)
		


