try:
    import json as simplejson
except ImportError:
    import simplejson

from pypodio2 import client

def json_response(resp):
	try:
		return simplejson.loads(resp)
	except:
		raise client.FailedRequest(resp)

def http_request(method, *args, **kwargs):
	print "Called"