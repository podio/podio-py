#!/usr/bin/env python
"""
Unit tests for pypodio2.areas.Item (via pypodio2.client.Client). Works
by mocking httplib2, and making assertions about how pypodio2 calls
it.
"""

try:
    import json
except ImportError:
    import simplejson as json

from mock import Mock
from nose.tools import eq_

from tests.utils import check_client_method, get_client_and_http, URL_BASE


def test_find():
    item_id = 9271

    client, check_assertions = check_client_method()
    result = client.Item.find(item_id)
    check_assertions(result, 'GET', '/item/%s' % item_id)

    client, check_assertions = check_client_method()
    result = client.Item.find(item_id, basic=True)
    check_assertions(result, 'GET', '/item/%s/basic' % item_id)


def test_filters():
    app_id = 426
    attributes = {'a': 1, 'zzzz': 12345}

    client, check_assertions = check_client_method()
    result = client.Item.filter(app_id, attributes)
    check_assertions(result,
                     'POST',
                     '/item/app/%s/filter/' % app_id,
                     expected_body=json.dumps(attributes),
                     expected_headers={'content-type': 'application/json'})


def test_find_by_external_id():
    app_id = 13
    external_id = 37

    client, check_assertions = check_client_method()
    result = client.Item.find_all_by_external_id(app_id, external_id)
    check_assertions(result,
                     'GET',
                     '/item/app/%s/v2/?external_id=%s' % (app_id, external_id))


def test_revisions():
    item_id = 255

    client, check_assertions = check_client_method()
    result = client.Item.revisions(item_id)
    check_assertions(result,
                     'GET',
                     '/item/%s/revision/' % (item_id))


def test_revision_difference():
    item_id = 2
    from_id = 4
    to_id = 8

    client, check_assertions = check_client_method()
    result = client.Item.revision_difference(item_id, from_id, to_id)
    check_assertions(result,
                     'GET',
                     '/item/%s/revision/%s/%s' % (item_id, from_id, to_id))


def test_values():
    item_id = 9271

    client, check_assertions = check_client_method()
    result = client.Item.values(item_id)
    check_assertions(result, 'GET', '/item/%s/value' % item_id)


def test_values_v2():
    item_id = 9271

    client, check_assertions = check_client_method()
    result = client.Item.values_v2(item_id)
    check_assertions(result, 'GET', '/item/%s/value/v2' % item_id)


def test_create():

    app_id = 1
    attributes = {'1': 1, '2': 3, '5': '8'}

    client, check_assertions = check_client_method()
    result = client.Item.create(app_id, attributes)
    check_assertions(result,
                     'POST',
                     '/item/app/%s/' % app_id,
                     json.dumps(attributes),
                     {'content-type': 'application/json'})


def test_update():
    app_id = 1
    attributes = {'1': 1, '2': 3, '5': '8'}

    client, check_assertions = check_client_method()
    result = client.Item.update(app_id, attributes)
    check_assertions(result,
                     'PUT',
                     '/item/%s' % app_id,
                     json.dumps(attributes),
                     {'content-type': 'application/json'})

    client, check_assertions = check_client_method()
    result = client.Item.update(app_id, attributes, silent=True)
    check_assertions(result,
                     'PUT',
                     '/item/%s?silent=true' % app_id,
                     json.dumps(attributes),
                     {'content-type': 'application/json'})


def test_delete():
    item_id = 1

    client, http = get_client_and_http()
    http.request = Mock(return_value=(None, None))

    result = client.Item.delete(item_id)

    eq_(None, result)
    http.request.assert_called_once_with("%s/item/%s?" % (URL_BASE, item_id),
                                         'DELETE',
                                         body=None,
                                         headers={})
