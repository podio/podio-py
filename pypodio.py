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


class API(object):
	'''Represents a Python interface to the Podio API.

	Usage:

	To create an instance of the API and get an OAuth Token
		>> import pypodio
		>> api = pypodio.API($api_secret, $api_key)
		>> api.request_oauth_token(username=$user, password = $username_password)
	
	Making a GET request to any API method is simple.
		>> api.req(url="$apiMethodURI", params={'$paramName':'$paramValue'})
	'''
		
	class OAuthToken(object):
		def __init__(self, resp):
			self.expires_at = resp['expires_in']
			self.access_token = resp['access_token']
			self.refresh_token = resp['refresh_token']

	def __init__(self, api_key=None,
	api_secret=None, base_url=None, debug=False):
		
		if base_url == None:
			self.base_url = "https://api.podio.com/"
		else:
			self.base_url = base_url
		
		if api_key == None or api_secret == None:
			raise PodioError("You must have an API key and secret to use the Podio API")
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
			self.headers.update({'authorization':"OAuth2 %s" % self.token.access_token})
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
			self.headers.update({'authorization':"OAuth2 %s" % self.token.access_token})
			return True
	
	def req(self, uri, method, *args, **kwargs):
		h = httplib2.Http()
		print self.headers
		if 'params' in kwargs:
			params = urlencode(kwargs['params'])
		else:
			params = ""
		
		if method.lower() == "get":
			resp, content = h.request("%s%s" % (self.base_url, uri), "GET",
				params, headers = self.headers)
		elif method.lower() == "post":
			headers = self.headers.update({'content-type':'application/x-www-form-urlencoded'})
			print headers #!!! Remove once debugged
			resp, content = h.request("%s%s" % (self.base_url, uri), "POST",
				params, headers = headers)
		elif method.lower() == "put":
			resp, content = h.request("%s%s" % (self.base_url, uri), "PUT",
				params, headers = self.headers)
		elif method.lower() == "delete":
			resp, content = h.request("%s%s" % (self.base_url, uri), "DELETE",
				params, headers = self.headers)
		if resp['status'] != '200':
			raise PodioError(content)
		return json.loads(content)

	# def __getattr__(self, name):
	# 	if name.startswith("get_"):
	# 		return lambda *args, **kwargs: self.req(name, *args, **kwargs)

	# 	raise AttributeError("%r object has no attribute %r" %
	# 		(type(self).__name__, name))

