from tenable.errors import *
from ..checker import check, single
import pytest, uuid

@pytest.fixture
def group(request, api):
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
    with pytest.raises(TypeError):
        api.groups.create(1)

@pytest.mark.vcr()
def test_groups_create(api, group):
    assert isinstance(group, dict)
    check(group, 'uuid', 'uuid')
    check(group, 'name', str)
    check(group, 'permissions', int)
    check(group, 'id', int)

@pytest.mark.vcr()
def test_groups_delete_id_typerror(api):
    with pytest.raises(TypeError):
        api.groups.delete('nothing')

@pytest.mark.vcr()
def test_groups_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.groups.delete(1)

@pytest.mark.vcr()
def test_groups_delete_success(api, group):
    api.groups.delete(group['id'])

@pytest.mark.vcr()
def test_groups_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.groups.edit('nope', 'something')

@pytest.mark.vcr()
def test_groups_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.groups.edit(1, 1)

@pytest.mark.vcr()
def test_groups_edit_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.groups.edit(1, 'newname')

@pytest.mark.vcr()
def test_groups_edit_success(api, group):
    edited = api.groups.edit(group['id'], 'New Example Name')
    assert isinstance(edited, dict)
    check(edited, 'uuid', 'uuid')
    check(edited, 'name', str)
    check(edited, 'permissions', int)
    check(edited, 'user_count', int)
    check(edited, 'id', int)

@pytest.mark.vcr()
def test_groups_list(api, group):
    groups = api.groups.list()
    assert isinstance(groups, list)
    for g in groups:
        assert isinstance(g, dict)
        check(g, 'id', int)
        check(g, 'name', str)
        check(g, 'permissions', int)
        check(g, 'user_count', int)
        check(g, 'uuid', 'uuid')

@pytest.mark.vcr()
def test_groups_list_users_id_typeerror(api):
    with pytest.raises(TypeError):
        api.groups.list_users('nope')

@pytest.mark.vcr()
def test_groups_list_users_notfound(api):
    with pytest.raises(NotFoundError):
        api.groups.list_users(1)

@pytest.mark.vcr()
def test_groups_list_users_success(api, group, user):
    api.groups.add_user(group['id'], user['id'])
    users = api.groups.list_users(group['id'])
    assert isinstance(users, list)
    for u in users:
        assert isinstance(u, dict)
        check(u, 'id', int)
        check(u, 'username', str)
        check(u, 'name', str)
        check(u, 'email', str)
        check(u, 'permissions', int)
        check(u, 'type', str)
        check(u, 'login_fail_count', int)
        check(u, 'login_fail_total', int)
        check(u, 'last_login_attempt', int)
        check(u, 'enabled', bool)
        check(u, 'uuid_id', 'uuid')

@pytest.mark.vcr()
def test_group_add_user_to_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.groups.add_user('nope', 1)

@pytest.mark.vcr()
def test_groups_add_user_to_group_user_id_typeerror(api):
    with pytest.raises(TypeError):
        api.groups.add_user(1, 'nope')

@pytest.mark.vcr()
def test_groups_add_user_to_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.groups.add_user(1, 1)

@pytest.mark.vcr()
def test_groups_add_user_to_group_success(api, group, user):
    api.groups.add_user(group['id'], user['id'])

@pytest.mark.vcr()
def test_groups_delete_user_from_group_group_id_tyupeerror(api):
    with pytest.raises(TypeError):
        api.groups.delete_user('nope', 1)

@pytest.mark.vcr()
def test_groups_delete_user_from_group_user_id_typeerror(api):
    with pytest.raises(TypeError):
        api.groups.delete_user(1, 'nope')

@pytest.mark.vcr()
def test_groups_delete_user_from_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.groups.delete_user(1, 1)

@pytest.mark.vcr()
def test_groups_delete_user_from_group_success(api, group, user):
    api.groups.add_user(group['id'], user['id'])
    api.groups.delete_user(group['id'], user['id'])