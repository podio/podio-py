'''A library exposing the Podio API as Python objects'''

__author__ = 'Nick Barnwell on behalf of Podio'
__version__ = '0.1'

import json
from urllib import urlencode
import httplib2

class PodioError(Exception):
	'''Base class for the API'''
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class API:
	'''Represents a Python interface to the Podio API.

	Usage:

	To create an instance of the API without credentials
		>>> import pypodio
		>>>	api = pypodio.API()

	'''
		
	class OAuthToken:
		def __init__(self, resp):
			self.expires_at = resp['expires_in']
			self.access_token = resp['access_token']
			self.refresh_token = resp['refresh_token']
		
	class request:
		def __init__(self, url, params, base_url, token):
			if params != None:
				self.params = params
			else:
				self.params = {}
						
			self.url = url
			self.base_url = base_url
			self.token = token
		
		def req(self):
			h = httplib2.Http()
			if self.params != None:
				params = urlencode(self.params)
			else:
				params = {}
			resp, content = h.request("%s%s" % (self.base_url, self.url), "GET", params, headers = {"authorization":"OAuth2 %s" % (self.token.access_token)})
			
			return content

	def __init__(self, api_key=None,
	api_secret=None, request_headers=None, base_url=None, debug=False):
		
		if base_url == None:
			self.base_url = "https://api.podio.com/"
		else:
			self.base_url = base_url
		
		if api_key == None or api_secret == None:
			raise Exception
		else:
			self.api_key = api_key
			self.api_secret = api_secret
			
		self.token = None
		self.headers = {}

	def request_oauth_token(self, username, password):
		h = httplib2.Http()

		data = urlencode(dict(
			grant_type="password", 
			client_id=self.api_key,
			client_secret=self.api_secret,
			username=username, 
			password=password)
		)

		resp, content = h.request("%soauth/token" % (self.base_url), "POST", data,
			headers = {'content-type':'application/x-www-form-urlencoded'})
		if resp['status'] != '200':
			raise PodioError(content)
		else:
			content = json.loads(content)
			self.token = self.OAuthToken(content)
			self.headers.update({'authorization':self.token.refresh_token})
			return self.token
	def refresh_oauth_token(self, token):
		'''Uses the refresh token to update the access token. 
		Takes an OAuthToken object'''
		
		h = httplib2.Http()

		data = urlencode(dict(
			grant_type="refresh_token", 
			client_id=self.api_key,
			client_secret=self.api_secret,
			refresh_token = token.refresh_token)
		)

		resp, content = h.request("%soauth/token" % (self.base_url), "POST", data,
			headers = {'content-type':'application/x-www-form-urlencoded'})
		if resp['status'] != '200':
			raise PodioError(content)
		else:
			content = json.loads(content)
			self.token = self.OAuthToken(content)
			self.headers.update({'authorization':self.token.refresh_token})
			return True
	
	def __getattr__(self, name, params = None):
		if name.startswith("get_"):
			url = '/'.join(name[4:].split('_'))
			req = self.request(url, params, base_url = self.base_url, token = self.token)
			return req.req()
		raise AttributeError("%r object has no attribute %r" %
        	(type(self).__name__, name))


	