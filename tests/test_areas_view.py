#!/usr/bin/env python
"""
Unit tests for pypodio2.areas.View (via pypodio2.client.Client). Works
by mocking httplib2, and making assertions about how pypodio2 calls
it.
"""

import json

from tests.utils import check_client_method


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


def test_get_view():
    app_id = 122
    view_id = 222
    view_name = 'pizzas4life'

    client, check_assertions = check_client_method()
    result = client.View.get(app_id, view_id)
    check_assertions(result, 'GET', '/view/app/{}/{}'.format(app_id, view_id))

    client, check_assertions = check_client_method()
    result = client.View.get(app_id, view_name)
    check_assertions(result, 'GET', '/view/app/{}/{}'.format(app_id, view_name))

    client, check_assertions = check_client_method()
    result = client.View.get(app_id, 'last')
    check_assertions(result, 'GET', '/view/app/{}/{}'.format(app_id, 'last'))


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

    view_id = 8675309
    client, check_assertions = check_client_method()
    result = client.View.make_default(view_id)
    check_assertions(result, 'POST', '/view/{}/default'.format(view_id),
                     expected_body=json.dumps({}),
                     expected_headers={'content-type': 'application/json'})


def test_update_last_view():
    app_id = 666777888
    attributes = {'a': 'b', 'c': 'd'}
    client, check_assertions = check_client_method()
    result = client.View.update_last_view(app_id, attributes)
    check_assertions(result, 'PUT', '/view/app/{}/last'.format(app_id),
                     expected_body=json.dumps(attributes),
                     expected_headers={'content-type': 'application/json'})


def test_update_view():
    view_id = 131314
    attributes = {'a': 'b', 'c': 'd'}
    client, check_assertions = check_client_method()
    result = client.View.update_view(view_id, attributes)
    check_assertions(result, 'PUT', '/view/{}'.format(view_id),
                     expected_body=json.dumps(attributes),
                     expected_headers={'content-type': 'application/json'})

