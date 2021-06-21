'''
test groups
'''
import uuid
import pytest
from tenable.errors import NotFoundError
from ..checker import check


@pytest.fixture(name='group_fixture')
def group(request, api):
    '''group fixture'''
    group = api.groups.create(str(uuid.uuid4()))

    def teardown():
        try:
            api.groups.delete(group['id'])
        except NotFoundError:
            pass

    request.addfinalizer(teardown)
    return group


@pytest.mark.vcr()
def test_groups_create_name_typeerror(api):
    '''test to raise the exception when type of name is not as defined'''
    with pytest.raises(TypeError):
        api.groups.create(1)


@pytest.mark.vcr()
def test_groups_create(api, group_fixture):
    '''test to create a group'''
    assert isinstance(group_fixture, dict)
    check(group_fixture, 'uuid', 'uuid')
    check(group_fixture, 'name', str)
    check(group_fixture, 'permissions', int)
    check(group_fixture, 'id', int)


@pytest.mark.vcr()
def test_groups_delete_id_typerror(api):
    '''test to raise the exception when type of id is not as defined'''
    with pytest.raises(TypeError):
        api.groups.delete('nothing')


@pytest.mark.vcr()
def test_groups_delete_notfounderror(api):
    '''test to raise the exception for deleting group that s not found'''
    with pytest.raises(NotFoundError):
        api.groups.delete(1)


@pytest.mark.vcr()
def test_groups_delete_success(api, group_fixture):
    '''test to delete the group'''
    api.groups.delete(group_fixture['id'])


@pytest.mark.vcr()
def test_groups_edit_id_typeerror(api):
    '''test to raise the exception when type of id is not as defined'''
    with pytest.raises(TypeError):
        api.groups.edit('nope', 'something')


@pytest.mark.vcr()
def test_groups_edit_name_typeerror(api):
    '''test to raise the exception when type of name is not as defined'''
    with pytest.raises(TypeError):
        api.groups.edit(1, 1)


@pytest.mark.vcr()
def test_groups_edit_notfounderror(api):
    '''test to raise the exception when tried to edit the group that is not found'''
    with pytest.raises(NotFoundError):
        api.groups.edit(1, 'newname')


@pytest.mark.vcr()
def test_groups_edit_success(api, group_fixture):
    '''test to edit the group'''
    edited = api.groups.edit(group_fixture['id'], 'New Example Name')
    assert isinstance(edited, dict)
    check(edited, 'uuid', 'uuid')
    check(edited, 'name', str)
    check(edited, 'permissions', int)
    check(edited, 'user_count', int)
    check(edited, 'id', int)


@pytest.mark.vcr()
def test_groups_list(api, group_fixture):
    '''test to get the list of groups'''
    groups = api.groups.list()
    assert isinstance(groups, list)
    for group in groups:
        assert isinstance(group, dict)
        check(group, 'id', int)
        check(group, 'name', str)
        check(group, 'permissions', int)
        check(group, 'user_count', int)
        check(group, 'uuid', 'uuid')


@pytest.mark.vcr()
def test_groups_list_users_id_typeerror(api):
    '''test to raise the exception when type of users id is not as defined'''
    with pytest.raises(TypeError):
        api.groups.list_users('nope')


@pytest.mark.vcr()
def test_groups_list_users_notfound(api):
    '''test to raise the exception when type of users is not as defined'''
    with pytest.raises(NotFoundError):
        api.groups.list_users(1)


@pytest.mark.vcr()
def test_groups_list_users_success(api, group_fixture, user):
    '''test to get the list of users'''
    api.groups.add_user(group_fixture['id'], user['id'])
    users = api.groups.list_users(group_fixture['id'])
    assert isinstance(users, list)
    for user in users:
        assert isinstance(user, dict)
        check(user, 'id', int)
        check(user, 'username', str)
        check(user, 'name', str)
        check(user, 'email', str)
        check(user, 'permissions', int)
        check(user, 'type', str)
        check(user, 'login_fail_count', int)
        check(user, 'login_fail_total', int)
        check(user, 'last_login_attempt', int)
        check(user, 'enabled', bool)
        check(user, 'uuid_id', 'uuid')


@pytest.mark.vcr()
def test_group_add_user_to_group_group_id_typeerror(api):
    '''test to raise the exception when type of group_id is not as defined'''
    with pytest.raises(TypeError):
        api.groups.add_user('nope', 1)


@pytest.mark.vcr()
def test_groups_add_user_to_group_user_id_typeerror(api):
    '''test to raise the exception when type of user_id is not as defined'''
    with pytest.raises(TypeError):
        api.groups.add_user(1, 'nope')


@pytest.mark.vcr()
def test_groups_add_user_to_group_notfounderror(api):
    '''test to raise the exception when tried to add the user to the group
    who is not found'''
    with pytest.raises(NotFoundError):
        api.groups.add_user(1, 1)


@pytest.mark.vcr()
def test_groups_add_user_to_group_success(api, group_fixture, user):
    '''test to add user to the group'''
    api.groups.add_user(group_fixture['id'], user['id'])


@pytest.mark.vcr()
def test_groups_delete_user_from_group_group_id_tyupeerror(api):
    '''test to raise the exception when type of group_id is not as defined'''
    with pytest.raises(TypeError):
        api.groups.delete_user('nope', 1)


@pytest.mark.vcr()
def test_groups_delete_user_from_group_user_id_typeerror(api):
    '''test to raise the exception when type of user_id is not as defined'''
    with pytest.raises(TypeError):
        api.groups.delete_user(1, 'nope')


@pytest.mark.vcr()
def test_groups_delete_user_from_group_notfounderror(api):
    '''test to raise the exception when user is not found to delete from the group'''
    with pytest.raises(NotFoundError):
        api.groups.delete_user(1, 1)


@pytest.mark.vcr()
def test_groups_delete_user_from_group_success(api, group_fixture, user):
    '''test to delete the user from the group'''
    api.groups.add_user(group_fixture['id'], user['id'])
    api.groups.delete_user(group_fixture['id'], user['id'])
