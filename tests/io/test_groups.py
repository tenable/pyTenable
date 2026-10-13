"""
test groups
"""

import pytest
import responses
from responses.matchers import json_params_matcher

from tenable.errors import NotFoundError
from tests.checker import check


@pytest.fixture(name='group')
def fixture_group():
    """
    Fixture to create group
    """
    return {
        'uuid': '00278150-35c2-40fc-8e47-fed17e23b68e',
        'name': 'b1f9aa26-0748-42e1-b0f0-d2b907511dc7',
        'permissions': 0,
        'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
        'id': 1,
    }


@responses.activate
def test_groups_create(tvm, group):
    """
    test to create group
    """
    responses.add(responses.POST, 'https://nourl/groups', json=group)
    group = tvm.groups.create(group['name'])
    assert isinstance(group, dict)
    check(group, 'uuid', 'uuid')
    check(group, 'name', str)
    check(group, 'id', int)


@responses.activate
def test_groups_delete_notfounderror(tvm):
    """
    test to raise exception when group_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/groups/1',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.groups.delete(1)


@responses.activate
def test_groups_delete_success(tvm, group):
    """
    test to delete group
    """
    responses.add(responses.DELETE, 'https://nourl/groups/1')
    tvm.groups.delete(group['id'])


@responses.activate
def test_groups_edit_notfounderror(tvm):
    """
    test to raise exception when group_id not found.
    """
    responses.add(
        responses.PUT,
        'https://nourl/groups/1',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.groups.edit(1, 'newname')


@responses.activate
def test_groups_edit_success(tvm, group):
    """
    test to edit group
    """
    responses.add(
        responses.PUT,
        'https://nourl/groups/1',
        json={
            'uuid': '00278150-35c2-40fc-8e47-fed17e23b68e',
            'name': 'New Example Name',
            'permissions': 0,
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'user_count': 0,
            'id': 1,
        },
    )
    edited = tvm.groups.edit(group['id'], 'New Example Name')
    assert isinstance(edited, dict)
    check(edited, 'uuid', 'uuid')
    check(edited, 'name', str)
    check(edited, 'user_count', int)
    check(edited, 'id', int)


@responses.activate
def test_groups_list(tvm):
    """
    test to get list of group
    """
    responses.add(
        responses.GET,
        'https://nourl/groups',
        json={
            'groups': [
                {
                    'uuid': '682a17d8-3b13-4657-9d28-8c344aaf836f',
                    'name': 'dd5fbe5d-4bdf-41bb-bf75-058c48e2682c',
                    'permissions': 0,
                    'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
                    'user_count': 0,
                    'id': 4,
                }
            ]
        },
    )
    groups = tvm.groups.list()
    assert isinstance(groups, list)
    for group in groups:
        assert isinstance(group, dict)
        check(group, 'id', int)
        check(group, 'name', str)
        check(group, 'user_count', int)
        check(group, 'uuid', 'uuid')


@responses.activate
def test_groups_list_users_notfound(tvm):
    """
    test to raise exception when user_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/groups/1/users',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.groups.list_users(1)


@responses.activate
def test_groups_list_users_success(tvm, group, user):
    """
    test to get list of users in group
    """
    responses.add(responses.POST, 'https://nourl/groups/1/users/3344')
    responses.add(
        responses.GET,
        'https://nourl/groups/1/users',
        json={
            'users': [
                {
                    'id': 3344,
                    'user_name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
                    'username': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
                    'email': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
                    'name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
                    'type': 'local',
                    'permissions': 64,
                    'last_login_attempt': 0,
                    'login_fail_count': 0,
                    'login_fail_total': 0,
                    'enabled': False,
                    'uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
                    'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
                    'uuid_id': '88aba081-9505-4e06-9acc-2530b486c8d4',
                }
            ]
        },
    )
    tvm.groups.add_user(group['id'], user['id'])
    users = tvm.groups.list_users(group['id'])
    assert isinstance(users, list)
    for usr in users:
        assert isinstance(usr, dict)
        check(usr, 'email', str)
        check(usr, 'enabled', bool)
        check(usr, 'id', int)
        check(usr, 'login_fail_count', int)
        check(usr, 'login_fail_total', int)
        check(usr, 'permissions', int)
        check(usr, 'type', str)
        check(usr, 'user_name', str)
        check(usr, 'username', str)
        check(usr, 'uuid_id', 'uuid')


@responses.activate
def test_groups_add_user_to_group_notfounderror(tvm):
    """
    test to raise exception when user_id or group_id not found.
    """
    responses.add(
        responses.POST,
        'https://nourl/groups/1/users/1',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.groups.add_user(1, 1)


@responses.activate
def test_groups_add_user_to_group_success(tvm, group, user):
    """
    test to add user group
    """
    responses.add(responses.POST, 'https://nourl/groups/1/users/3344')
    tvm.groups.add_user(group['id'], user['id'])


@responses.activate
def test_groups_delete_user_from_group_notfounderror(tvm):
    """
    test to raise exception when user_id or group_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/groups/1/users/1',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.groups.delete_user(1, 1)


@responses.activate
def test_groups_delete_user_from_group_success(tvm, group, user):
    """
    test to delete user from group
    """
    responses.add(responses.POST, 'https://nourl/groups/1/users/3344')
    responses.add(responses.DELETE, 'https://nourl/groups/1/users/3344')
    tvm.groups.add_user(group['id'], user['id'])
    tvm.groups.delete_user(group['id'], user['id'])


GROUP = {
    'uuid': 'd4e5f6a7-b8c9-0123-def4-567890abcdef',
    'name': 'SAML Admins',
    'id': 1130088,
    'container_uuid': 'c1d2e3f4-a5b6-7890-cdef-123456789abc',
}


@responses.activate
@pytest.mark.parametrize(
    'kwargs, body',
    [
        ({}, {'name': 'SAML Admins'}),
        ({'managed_by_saml': True}, {'name': 'SAML Admins', 'managed_by_saml': True}),
        ({'managed_by_saml': False}, {'name': 'SAML Admins', 'managed_by_saml': False}),
    ],
)
def test_groups_create_managed_by_saml(tvm, kwargs, body):
    responses.post(
        'https://nourl/groups',
        json={**GROUP, **kwargs},
        match=[json_params_matcher(body, strict_match=True)],
    )
    assert tvm.groups.create('SAML Admins', **kwargs) == {**GROUP, **kwargs}


@responses.activate
@pytest.mark.parametrize(
    'kwargs, body',
    [
        ({}, {'name': 'SAML Admins'}),
        ({'managed_by_saml': True}, {'name': 'SAML Admins', 'managed_by_saml': True}),
        ({'managed_by_saml': False}, {'name': 'SAML Admins', 'managed_by_saml': False}),
    ],
)
def test_groups_edit_managed_by_saml(tvm, kwargs, body):
    responses.put(
        'https://nourl/groups/1130088',
        json={**GROUP, **kwargs},
        match=[json_params_matcher(body, strict_match=True)],
    )
    assert tvm.groups.edit(1130088, 'SAML Admins', **kwargs) == {**GROUP, **kwargs}


@responses.activate
@pytest.mark.parametrize('method', ['create', 'edit'])
@pytest.mark.parametrize('value', ['maybe', 1])
def test_groups_managed_by_saml_typeerror(tvm, method, value):
    args = ('SAML Admins',) if method == 'create' else (1130088, 'SAML Admins')
    with pytest.raises(TypeError):
        getattr(tvm.groups, method)(*args, managed_by_saml=value)
    assert len(responses.calls) == 0


@pytest.mark.parametrize('method', ['create', 'edit'])
def test_groups_managed_by_saml_keyword_only(tvm, method):
    args = ('SAML Admins',) if method == 'create' else (1130088, 'SAML Admins')
    with pytest.raises(TypeError):
        getattr(tvm.groups, method)(*args, True)
