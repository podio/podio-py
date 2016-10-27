#!/usr/bin/env python
"""
Unit tests for pypodio2.areas.View (via pypodio2.client.Client). Works
by mocking httplib2, and making assertions about how pypodio2 calls
it.
"""

import json

from mock import Mock
from nose.tools import eq_

from tests.utils import check_client_method, get_client_and_http, URL_BASE


def test_create():
    app_id = 12345
    view_details = {}

    client, check_assertions = check_client_method()
    result = client.View.create(app_id, view_details)
    check_assertions(result, 'POST', '/view/app/{}/'.format(app_id),
                     json.dumps(view_details),
                     {'content-type': 'application/json'})


def test_delete():
    view_id = 67423

    client, check_assertions = check_client_method()
    result = client.View.delete(view_id)
    check_assertions(result, 'DELETE', '/view/{}'.format(view_id))


def test_get():
    pass


def test_get_views():

    app_id = 12346789
    client, check_assertions = check_client_method()
    result = client.View.get_views(app_id)
    check_assertions(result, 'GET', '/view/app/{}/?include_standard_views=false'.format(app_id))

    client, check_assertions = check_client_method()
    result = client.View.get_views(app_id, True)
    check_assertions(result, 'GET', '/view/app/{}/?include_standard_views=true'.format(app_id))

    client, check_assertions = check_client_method()
    result = client.View.get_views(app_id, False)
    check_assertions(result, 'GET', '/view/app/{}/?include_standard_views=false'.format(app_id))


def test_make_default():
    pass


def test_update_last_view():
    pass


def test_update_view():
    pass
