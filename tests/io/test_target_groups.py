from .fixtures import *
from tenable.errors import *

@pytest.fixture
def targetgroup(request, api):
    group = api.target_groups.create(str(uuid.uuid4()), ['192.168.0.1'])
    def teardown():
        try:
            api.target_groups.delete(group['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return group

def test_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.create(False, [])

def test_create_type_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.create('nope', [], type=1)

def test_create_type_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.target_groups.create('nope', [], type='nope')

def test_create_acls_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.create('nope', [], acls='nope')

def test_create_members_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.target_groups.create('nope', [])

def test_create(api, targetgroup):
    assert isinstance(targetgroup, dict)
    t = targetgroup
    check(t, 'acls', list)
    for a in t['acls']:
        check(a, 'display_name', str, allow_none=True)
        check(a, 'id', int, allow_none=True)
        check(a, 'name', str, allow_none=True)
        check(a, 'owner', int, allow_none=True)
        check(a, 'permissions', int)
        check(a, 'type', str)
    check(t, 'creation_date', int)
    check(t, 'default_group', int)
    check(t, 'id', int)
    check(t, 'last_modification_date', int)
    check(t, 'members', str)
    check(t, 'name', str)
    check(t, 'owner', str)
    check(t, 'owner_id', int)
    check(t, 'shared', int)
    check(t, 'user_permissions', int)

def test_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.delete('nope')

def test_delete(api, targetgroup):
    pass

def test_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.details('nope')

def test_details(api, targetgroup):
    group = api.target_groups.details(targetgroup['id'])
    assert isinstance(group, dict)
    assert group['id'] == targetgroup['id']
    t = group
    check(t, 'acls', list)
    for a in t['acls']:
        check(a, 'display_name', str, allow_none=True)
        check(a, 'id', int, allow_none=True)
        check(a, 'name', str, allow_none=True)
        check(a, 'owner', int, allow_none=True)
        check(a, 'permissions', int)
        check(a, 'type', str)
    check(t, 'creation_date', int)
    check(t, 'default_group', int)
    check(t, 'id', int)
    check(t, 'last_modification_date', int)
    check(t, 'members', str)
    check(t, 'name', str)
    check(t, 'owner', str)
    check(t, 'owner_id', int)
    check(t, 'shared', int)
    check(t, 'user_permissions', int)

def test_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.delete('nope')

def test_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.edit(1, 1)

def test_edit_acls_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.edit(1, acls=False)

def test_edit_type_typeerror(api):
    with pytest.raises(TypeError):
        api.target_groups.edit(1, type=False)

def test_edit_type_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.target_groups.edit(1, type='nope')

def test_edit(api, targetgroup):
    members = targetgroup['members'].split(',')
    members.append('192.168.0.2')
    mod = api.target_groups.edit(targetgroup['id'], members=members)
    assert isinstance(mod, dict)
    t = mod
    check(t, 'acls', list)
    for a in t['acls']:
        check(a, 'display_name', str, allow_none=True)
        check(a, 'id', int, allow_none=True)
        check(a, 'name', str, allow_none=True)
        check(a, 'owner', int, allow_none=True)
        check(a, 'permissions', int)
        check(a, 'type', str)
    check(t, 'creation_date', int)
    check(t, 'default_group', int)
    check(t, 'id', int)
    check(t, 'last_modification_date', int)
    check(t, 'members', str)
    check(t, 'name', str)
    check(t, 'owner', str)
    check(t, 'owner_id', int)
    check(t, 'shared', int)
    check(t, 'user_permissions', int)
    assert mod['members'] == ', '.join(members)

def test_list(api):
    assert isinstance(api.target_groups.list(), list)