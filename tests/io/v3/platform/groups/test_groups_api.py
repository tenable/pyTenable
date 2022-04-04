'''
Testing the Groups endpoints
'''
import responses
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL = 'https://cloud.tenable.com'
GROUPS_BASE_URL = f'{BASE_URL}/api/v3/groups'
GROUP_ID = '95ecc380-afe9-11e4-9b6c-751b66dd541e'
USER_ID = 'e9f23194-adb7-4c02-8632-615c694c787e'


@responses.activate
def test_add_user(api):
    responses.add(
        responses.POST,
        f'{GROUPS_BASE_URL}/{GROUP_ID}/users/{USER_ID}'
    )

    responses.add(
        responses.GET,
        f'{GROUPS_BASE_URL}/{GROUP_ID}/users',
        json={
            'users': [
                {
                    'id': USER_ID,
                    'username': 'test.user@tenable.com',
                    'email': 'test.user@tenable.com',
                    'name': 'test.user@tenable.com',
                    'type': 'local',
                    'permissions': 64,
                    'login_fail_count': 0,
                    'login_fail_total': 0,
                    'last_apikey_access': 1636464654829,
                    'enabled': True,
                    'lockout': 0,
                    'lastlogin': 1635924062814,
                },
                {
                    'id': 'd3402235-7fa2-49e1-9a8f-15e97707c929',
                    'username': 'test.user2@tenable.com',
                    'email': 'test.user2@tenable.com',
                    'name': 'test.user2@tenable.com',
                    'type': 'local',
                    'permissions': 64,
                    'login_fail_count': 0,
                    'login_fail_total': 0,
                    'enabled': True,
                    'lockout': 0,
                },
            ]
        },
    )

    resp = api.v3.platform.groups.add_user(GROUP_ID, USER_ID)
    user_ids = [user['id'] for user in resp]

    assert USER_ID in user_ids


@responses.activate
def test_create(api):
    group_name = 'Test Group'
    responses.add(
        responses.POST,
        f'{GROUPS_BASE_URL}',
        match=[responses.matchers.json_params_matcher({'name': group_name})],
        json={
            'id': GROUP_ID,
            'name': group_name,
        },
    )
    resp = api.v3.platform.groups.create(group_name)
    assert resp['name'] == group_name
    assert resp['id'] == GROUP_ID


@responses.activate
def test_delete(api):
    responses.add(responses.DELETE, f'{GROUPS_BASE_URL}/{GROUP_ID}')
    assert None is api.v3.platform.groups.delete(GROUP_ID)


@responses.activate
def test_delete_user(api):
    responses.add(
        responses.DELETE,
        f'{GROUPS_BASE_URL}/{GROUP_ID}/users/{USER_ID}'
    )
    assert None is api.v3.platform.groups.delete_user(GROUP_ID, USER_ID)


@responses.activate
def test_edit(api):
    updated_group_name = 'Updated Test Group'

    api_payload = {'name': updated_group_name}
    responses.add(
        responses.PUT,
        f'{GROUPS_BASE_URL}/{GROUP_ID}',
        match=[responses.matchers.json_params_matcher(api_payload)],
        json={'id': GROUP_ID, 'name': updated_group_name, 'user_count': 0},
    )

    resp = api.v3.platform.groups.edit(GROUP_ID, updated_group_name)
    assert resp['id'] == GROUP_ID
    assert resp['name'] == updated_group_name


@responses.activate
def test_list_users(api):

    responses.add(
        responses.GET,
        f'{GROUPS_BASE_URL}/{GROUP_ID}/users',
        json={
            'users': [
                {
                    'id': USER_ID,
                    'username': 'test.user@tenable.com',
                    'email': 'test.user@tenable.com',
                    'name': 'test.user@tenable.com',
                    'type': 'local',
                    'permissions': 64,
                    'login_fail_count': 0,
                    'login_fail_total': 0,
                    'last_apikey_access': 1636464654829,
                    'enabled': True,
                    'lockout': 0,
                    'lastlogin': 1635924062814,
                },
                {
                    'id': 'd3402235-7fa2-49e1-9a8f-15e97707c929',
                    'username': 'test.user2@tenable.com',
                    'email': 'test.user2@tenable.com',
                    'name': 'test.user2@tenable.com',
                    'type': 'local',
                    'permissions': 64,
                    'login_fail_count': 0,
                    'login_fail_total': 0,
                    'enabled': True,
                    'lockout': 0,
                },
            ]
        },
    )

    resp = api.v3.platform.groups.list_users(GROUP_ID)
    assert resp[0]['id'] == USER_ID
    assert resp[0]['enabled']
    assert resp[0]['name'] == 'test.user@tenable.com'


@responses.activate
def test_search(api):
    '''
    Test the search function
    '''
    response = {
        'groups': [
            {
                'id': '00000000-0000-0000-0000-000000000000',
                'name': 'All Users',
                'user_count': 2,
                'permissions': 'null',
                'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297'
            }
        ]
    }
    fields = [
        'id',
        'name',
        'user_count'
    ]
    filters = {
        'and': [
            {
                'property': 'user_count',
                'operator': 'gt',
                'value': 0
            }
        ]
    }

    api_payload = {
        'fields': fields,
        'filter': filters,
        'limit': 2
    }

    responses.add(
        responses.POST,
        f'{GROUPS_BASE_URL}/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )
    resp = api.v3.platform.groups.search(
        fields=fields,
        filter=filters,
        limit=2
    )
    assert isinstance(resp, SearchIterator)

    for ind, group in enumerate(resp):
        assert group == response['groups'][ind]

    resp = api.v3.platform.groups.search(
        fields=fields,
        filter=filters,
        limit=2,
        return_csv=True
    )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.platform.groups.search(
        fields=fields,
        filter=filters,
        limit=2,
        return_resp=True
    )
    assert isinstance(resp, Response)
