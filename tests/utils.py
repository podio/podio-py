"""
Helper methods for testing
"""
import json

from uuid import uuid4

from mock import Mock
from nose.tools import eq_

import pypodio2.client
import pypodio2.transport

# Just in case actual HTTP calls are made, don't use a real URL
URL_BASE = 'https://api.example.com'


def get_client_and_http():
    """
    Gets a pypodio2.client.Client instance and a mocked instance of
    httplib2.Http that backs it. Returned as (client, Http)
    """
    transport = pypodio2.transport.HttpTransport(
        URL_BASE, headers_factory=dict)
    client = pypodio2.client.Client(transport)

    http = Mock()
    transport._http = http

    return client, http


# This is used a lot by test_areas_*. It's a little weird, but it
# reduces the amount of code to write per test by a lot.
def check_client_method():
    """
    Helper to test an API method -- returns a tuple of
    (test_api_client, check_assertions) where check_assertions will
    verify that the API method returned the data from http.request,
    and that http.request was called with the correct arguments.

    check_assertions' signature is:
    def check_assertions(object_returned_from_api,
                         # GET, POST, etc.
                         http_method,
                         # Include the leading /
                         expected_path,
                         # Assert that this string was sent as the request body
                         expected_body,
                         # Assert that the request headers match this dict
                         expected_headers)

    To assert that client.Org().get_all calls URL_BASE/org/ and
    is correctly hooked up to http.request():

        client, check_assertions = check_client_method()
        result = client.Org.get_all()
        check_assertions(result, 'GET', '/org/')

    You can also pass body and headers to check_assertions.
    """
    client, http = get_client_and_http()
    returned_object = {'uuid': uuid4().hex}

    response = Mock()
    response.status = 200
    http.request = Mock(return_value=(
        response, json.dumps(returned_object).encode("utf-8")))

    def check_assertions(actual_returned,
                         http_method,
                         expected_path,
                         expected_body=None,
                         expected_headers=None):
        if expected_headers is None:
            expected_headers = {}

        eq_(returned_object,
            actual_returned,
            "API method didn't return the same object as http.request()")
        http.request.assert_called_once_with(URL_BASE + expected_path,
                                             http_method,
                                             body=expected_body,
                                             headers=expected_headers)

    return client, check_assertions
