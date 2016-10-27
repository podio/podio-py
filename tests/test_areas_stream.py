#!/usr/bin/env python

"""
Unit tests for pypodio2.areas.Stream (via pypodio2.client.Client). Works
by mocking httplib2, and making assertions about how pypodio2 calls
it.
"""


from tests.utils import check_client_method


def test_find_all():
    client, check_assertions = check_client_method()
    result = client.Stream.find_all()
    check_assertions(result, 'GET', '/stream/')


def test_find_all_by_org_id():
    org_id = 81076

    client, check_assertions = check_client_method()
    result = client.Stream.find_all_by_org_id(org_id)
    check_assertions(result, 'GET', '/stream/org/%s/' % org_id)


def test_find_all_personal():
    client, check_assertions = check_client_method()
    result = client.Stream.find_all_personal()
    check_assertions(result, 'GET', '/stream/personal/')


def test_find_all_by_space_id():
    space_id = 2222

    client, check_assertions = check_client_method()
    result = client.Stream.find_all_by_space_id(space_id)
    check_assertions(result, 'GET', '/stream/space/%s/' % space_id)


def test_find_by_ref():
    # It's not entirely clear what inputs are appropriate for ref_type.
    # But for this test's purposes, any string will do.
    ref_type = 'item'
    ref_id = 10203

    client, check_assertions = check_client_method()
    result = client.Stream.find_by_ref(ref_type, ref_id)
    check_assertions(result, 'GET', '/stream/%s/%s' % (ref_type, ref_id))


def test_find_item_by_external_id():
    app_id = 13
    external_id = 37

    client, check_assertions = check_client_method()
    result = client.Item.find_all_by_external_id(app_id, external_id)
    check_assertions(result,
                     'GET',
                     '/item/app/%s/v2/?external_id=%s' % (app_id, external_id))


def test_item_revisions():
    item_id = 255

    client, check_assertions = check_client_method()
    result = client.Item.revisions(item_id)
    check_assertions(result,
                     'GET',
                     '/item/%s/revision/' % item_id)


def test_item_revision_difference():
    item_id = 2
    from_id = 4
    to_id = 8

    client, check_assertions = check_client_method()
    result = client.Item.revision_difference(item_id, from_id, to_id)
    check_assertions(result,
                     'GET',
                     '/item/%s/revision/%s/%s' % (item_id, from_id, to_id))


def test_item_revision_difference():
    item_id = 2
    from_id = 4
    to_id = 8

    client, check_assertions = check_client_method()
