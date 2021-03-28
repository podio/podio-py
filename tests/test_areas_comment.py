#!/usr/bin/env python
"""
Unit tests for pypodio2.areas.Comment (via pypodio2.client.Client). Works
by mocking httplib2, and making assertions about how pypodio2 calls
it.
"""

import json

from mock import Mock
from nose.tools import eq_

from tests.utils import check_client_method, get_client_and_http, URL_BASE


def test_find_all():
    client, check_assertions = check_client_method()
    result = client.Comment.find_all()
    check_assertions(result, 'GET', '/comment/')


def test_find():
    comment_id = 9271

    client, check_assertions = check_client_method()
    result = client.Comment.find(comment_id)
    check_assertions(result, 'GET', '/comment/%s' % comment_id)


def test_find_all_for():
    commentable_type = 'Item'
    commentable_id = 3984

    client, check_assertions = check_client_method()
    result = client.Comment.find_all_for(commentable_type, commentable_id)
    check_assertions(result, 'GET', '/comment/%s/%s' % (commentable_type, commentable_id))


def test_find_recent_for_share():
    client, check_assertions = check_client_method()
    result = client.Comment.find_recent_for_share()
    check_assertions(result, 'GET', '/comment/share/')


def test_liked_by():
    comment_id = 9271

    client, check_assertions = check_client_method()
    result = client.Comment.liked_by(comment_id)
    check_assertions(result, 'GET', '/comment/%s/liked_by/' % comment_id)


def test_create():
    commentable_type = 'Item'
    commentable_id = 3984
    attributes = {'1': 1, '2': 3, '5': '8'}

    client, check_assertions = check_client_method()
    result = client.Comment.create(commentable_type, commentable_id, attributes)
    check_assertions(result,
                     'POST',
                     '/comment/%s/%s' % (commentable_type, commentable_id),
                     expected_body=json.dumps(attributes),
                     expected_headers={'content-type': 'application/json'})


def test_update():
    comment_id = 9271
    attributes = {'1': 1, '2': 3, '5': '8'}

    client, check_assertions = check_client_method()
    result = client.Comment.update(comment_id, attributes)
    check_assertions(result,
                     'POST',
                     '/comment/%s' % comment_id,
                     expected_body=json.dumps(attributes),
                     expected_headers={'content-type': 'application/json'})


def test_delete():
    comment_id = 1

    client, http = get_client_and_http()
    http.request = Mock(return_value=(None, None))

    result = client.Comment.delete(comment_id)

    eq_(None, result)
    http.request.assert_called_once_with("%s/comment/%s?" % (URL_BASE, comment_id),
                                         'DELETE',
                                         body=None,
                                         headers={})
