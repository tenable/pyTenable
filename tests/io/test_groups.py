'''
test groups
'''
import uuid
import pytest
from tenable.errors import NotFoundError
from tests.checker import check

@pytest.fixture(name='group')
def fixture_group(request, api):
    '''
    Fixture to create group
    '''
    group = api.groups.create(str(uuid.uuid4()))

    def teardown():
        '''
        cleanup function to delete group
        '''
        try:
            api.groups.delete(group['id'])
        except NotFoundError:
            pass

    request.addfinalizer(teardown)
    return group


@pytest.mark.vcr()
def test_groups_create_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.create(1)


@pytest.mark.vcr()
def test_groups_create(group):
    '''
    test to create group
    '''
    assert isinstance(group, dict)
    check(group, 'uuid', 'uuid')
    check(group, 'name', str)
    check(group, 'id', int)

@pytest.mark.vcr()
def test_groups_delete_id_typerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.delete('nothing')


@pytest.mark.vcr()
def test_groups_delete_notfounderror(api):
    '''
    test to raise exception when group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.groups.delete(1)


@pytest.mark.vcr()
def test_groups_delete_success(api, group):
    '''
    test to delete group
    '''
    api.groups.delete(group['id'])

@pytest.mark.vcr()
def test_groups_edit_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.edit('nope', 'something')

@pytest.mark.vcr()
def test_groups_edit_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.edit(1, 1)

@pytest.mark.vcr()
def test_groups_edit_notfounderror(api):
    '''
    test to raise exception when group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.groups.edit(1, 'newname')

@pytest.mark.vcr()
def test_groups_edit_success(api, group):
    '''
    test to edit group
    '''
    edited = api.groups.edit(group['id'], 'New Example Name')
    assert isinstance(edited, dict)
    check(edited, 'uuid', 'uuid')
    check(edited, 'name', str)
    check(edited, 'user_count', int)
    check(edited, 'id', int)

@pytest.mark.vcr()
def test_groups_list(api):
    '''
    test to get list of group
    '''
    groups = api.groups.list()
    assert isinstance(groups, list)
    for group in groups:
        assert isinstance(group, dict)
        check(group, 'id', int)
        check(group, 'name', str)
        check(group, 'user_count', int)
        check(group, 'uuid', 'uuid')

@pytest.mark.vcr()
def test_groups_list_users_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.list_users('nope')

@pytest.mark.vcr()
def test_groups_list_users_notfound(api):
    '''
    test to raise exception when user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.groups.list_users(1)

@pytest.mark.vcr()
def test_groups_list_users_success(api, group, user):
    '''
    test to get list of users in group
    '''
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
def test_group_add_user_to_group_group_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.add_user('nope', 1)


@pytest.mark.vcr()
def test_groups_add_user_to_group_user_id_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.add_user(1, 'nope')


@pytest.mark.vcr()
def test_groups_add_user_to_group_notfounderror(api):
    '''
    test to raise exception when user_id or group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.groups.add_user(1, 1)


@pytest.mark.vcr()
def test_groups_add_user_to_group_success(api, group, user):
    '''
    test to add user group
    '''
    api.groups.add_user(group['id'], user['id'])

@pytest.mark.vcr()
def test_groups_delete_user_from_group_group_id_tyupeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.delete_user('nope', 1)


@pytest.mark.vcr()
def test_groups_delete_user_from_group_user_id_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.groups.delete_user(1, 'nope')


@pytest.mark.vcr()
def test_groups_delete_user_from_group_notfounderror(api):
    '''
    test to raise exception when user_id or group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.groups.delete_user(1, 1)


@pytest.mark.vcr()
def test_groups_delete_user_from_group_success(api, group, user):
    '''
    test to delete user from group
    '''
    api.groups.add_user(group['id'], user['id'])
    api.groups.delete_user(group['id'], user['id'])
