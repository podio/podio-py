#!/usr/bin/env python
"""
Unit tests for pypodio2.areas.Comment (via pypodio2.client.Client). Works
by mocking httplib2, and making assertions about how pypodio2 calls
it.
"""

import json

from tests.utils import check_client_method


def test_create():
    item_id = 12345
    ref_type = "item"
    attributes = {"values":"test value"}

    client, check_assertions = check_client_method()
    result = client.Comment.create(ref_type,item_id,attributes)
    check_assertions(result, 'POST', '/comment/{}/{}/'.format(ref_type,item_id),
                     json.dumps(attributes),
                     {'content-type': 'application/json'})

def test_update():

    comment_id= 1231231
    attributes= {"value" : "New updated value"}

    client, check_assertions = check_client_method()
    result = client.Comment.update(comment_id, attributes)
    check_assertions(result,
                     'PUT',
                     '/comment/%d' % comment_id,
                     json.dumps(attributes),
                     {'content-type': 'application/json'})

    client, check_assertions = check_client_method()
    result = client.Comment.update(comment_id, attributes, silent=True)
    check_assertions(result,
                     'PUT',
                     '/comment/%s?silent=true' % comment_id,
                     json.dumps(attributes),
                     {'content-type': 'application/json'})

def test_find():
    comment_id = 67423

    client, check_assertions = check_client_method()
    result = client.Comment.find(comment_id)
    check_assertions(result, 'GET', '/comment/{}'.format(comment_id))

def test_find_all():
    item_id = 67423
    ref_type = "item"

    client, check_assertions = check_client_method()
    result = client.Comment.find_all(ref_type,item_id)
    check_assertions(result, 'GET', '/comment/{}/{}'.format(ref_type, item_id))

def test_revisions():
    comment_id = 67423

    client, check_assertions = check_client_method()
    result = client.Comment.revisions(comment_id)
    check_assertions(result, 'GET', '/comment/{}/revision'.format(comment_id))

def test_delete():
    comment_id = 67423

    client, check_assertions = check_client_method()
    result = client.Comment.delete(comment_id)
    check_assertions(result, 'DELETE', '/comment/{}'.format(comment_id))