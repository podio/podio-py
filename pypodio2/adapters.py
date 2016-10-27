
import json

from .client import FailedRequest


def json_response(resp):
    try:
        return json.loads(resp)
    except:
        raise FailedRequest(resp)


def http_request(method, *args, **kwargs):
    print("Called")
