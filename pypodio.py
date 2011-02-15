'''A library exposing the Podio API as Python objects'''

__author__ = 'Nick Barnwell'
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

	To create an instance of the API without credentials
		>>> import pypodio
		>>>	api = pypodio.API()

	'''
	class OAuthToken(object):
		def __init__(self, resp):
			self.expires_at = resp['expires_in']
			self.access_token = resp['access_token']
			self.refresh_token = resp['refresh_token']


	def __init__(self, api_key=None,
	api_secret=None, request_headers=None, base_url=None, debug=False):
		
		if base_url == None:
			self.base_url = "https://api.podio.com"
		else:
			self.base_url = base_url
		
		if api_key == None or api_secret == None:
			raise Exception
		else:
			self.api_key = api_key
			self.api_secret = api_secret
			
		self.token = None
		self.headers = {}

	def get_auth_token(self, username, password):
		h = httplib2.Http()

		data = urlencode(dict(
			grant_type="password", 
			client_id=self.api_key,
			client_secret=self.api_secret,
			username=username, 
			password=password)
		)

		resp, content = h.request("%s/oauth/token" % (self.base_url), "POST", data,
			headers = {'content-type':'application/x-www-form-urlencoded'})
		if resp['status'] != '200':
			raise PodioError(content)
		else:
			content = json.loads(content)
			self.token = self.OAuthToken(content)
			self.headers.update({'authorization':self.token.refresh_token})
			return self.token
	def refresh_access_token(self, token):
		'''Uses the refresh token to update the access token. 
		Takes an OAuthToken object'''
		
		h = httplib2.Http()

		data = urlencode(dict(
			grant_type="refresh_token", 
			client_id=self.api_key,
			client_secret=self.api_secret,
			refresh_token = token.refresh_token)
		)

		resp, content = h.request("%s/oauth/token" % (self.base_url), "POST", data,
			headers = {'content-type':'application/x-www-form-urlencoded'})
		if resp['status'] != '200':
			raise PodioError(content)
		else:
			content = json.loads(content)
			self.token = self.OAuthToken(content)
			self.headers.update({'authorization':self.token.refresh_token})
			return True