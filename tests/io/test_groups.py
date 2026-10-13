"""
test groups
"""

import uuid

import pytest
import responses
from responses.matchers import json_params_matcher

from tenable.errors import NotFoundError
from tests.checker import check
from tests.pytenable_log_handler import log_exception


@pytest.fixture(name='group')
def fixture_group(request, api):
    """
    Fixture to create group
    """
    group = api.groups.create(str(uuid.uuid4()))

    def teardown():
        """
        cleanup function to delete group
        """
        try:
            api.groups.delete(group['id'])
        except NotFoundError as err:
            log_exception(err)
            pass

    request.addfinalizer(teardown)
    return group


@pytest.mark.vcr()
def test_groups_create(group):
    """
    test to create group
    """
    assert isinstance(group, dict)
    check(group, 'uuid', 'uuid')
    check(group, 'name', str)
    check(group, 'id', int)


@pytest.mark.vcr()
def test_groups_delete_notfounderror(api):
    """
    test to raise exception when group_id not found.
    """
    with pytest.raises(NotFoundError):
        api.groups.delete(1)


@pytest.mark.vcr()
def test_groups_delete_success(api, group):
    """
    test to delete group
    """
    api.groups.delete(group['id'])


@pytest.mark.vcr()
def test_groups_edit_notfounderror(api):
    """
    test to raise exception when group_id not found.
    """
    with pytest.raises(NotFoundError):
        api.groups.edit(1, 'newname')


@pytest.mark.vcr()
def test_groups_edit_success(api, group):
    """
    test to edit group
    """
    edited = api.groups.edit(group['id'], 'New Example Name')
    assert isinstance(edited, dict)
    check(edited, 'uuid', 'uuid')
    check(edited, 'name', str)
    check(edited, 'user_count', int)
    check(edited, 'id', int)


@pytest.mark.vcr()
def test_groups_list(api):
    """
    test to get list of group
    """
    groups = api.groups.list()
    assert isinstance(groups, list)
    for group in groups:
        assert isinstance(group, dict)
        check(group, 'id', int)
        check(group, 'name', str)
        check(group, 'user_count', int)
        check(group, 'uuid', 'uuid')


@pytest.mark.vcr()
def test_groups_list_users_notfound(api):
    """
    test to raise exception when user_id not found.
    """
    with pytest.raises(NotFoundError):
        api.groups.list_users(1)


@pytest.mark.vcr()
def test_groups_list_users_success(api, group, user):
    """
    test to get list of users in group
    """
    api.groups.add_user(group['id'], user['id'])
    users = api.groups.list_users(group['id'])
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


@pytest.mark.vcr()
def test_groups_add_user_to_group_notfounderror(api):
    """
    test to raise exception when user_id or group_id not found.
    """
    with pytest.raises(NotFoundError):
        api.groups.add_user(1, 1)


@pytest.mark.vcr()
def test_groups_add_user_to_group_success(api, group, user):
    """
    test to add user group
    """
    api.groups.add_user(group['id'], user['id'])


@pytest.mark.vcr()
def test_groups_delete_user_from_group_notfounderror(api):
    """
    test to raise exception when user_id or group_id not found.
    """
    with pytest.raises(NotFoundError):
        api.groups.delete_user(1, 1)


@pytest.mark.vcr()
def test_groups_delete_user_from_group_success(api, group, user):
    """
    test to delete user from group
    """
    api.groups.add_user(group['id'], user['id'])
    api.groups.delete_user(group['id'], user['id'])


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
