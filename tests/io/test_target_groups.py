'''
test target groups
'''
import uuid
import pytest
from tenable.errors import NotFoundError, UnexpectedValueError
from ..checker import check


@pytest.fixture
@pytest.mark.vcr()
def targetgroup(request, api):
    '''
    target group fixture
    '''
    group = api.target_groups.create(str(uuid.uuid4()), ['192.168.0.1'])

    def teardown():
        try:
            api.target_groups.delete(group['id'])
        except NotFoundError:
            pass

    request.addfinalizer(teardown)
    return group


@pytest.mark.vcr()
def test_targetgroups_create_type_unexpectedvalue(api):
    '''
    test to raise the exception when value of type is not as defined
    '''
    with pytest.raises(UnexpectedValueError):
        api.target_groups.create('nope', [], type='nope')


@pytest.mark.vcr()
def test_targetgroups_create_acls_typeerror(api):
    '''
    test to raise the exception when value of acls is not as defined
    '''
    with pytest.raises(TypeError):
        api.target_groups.create('nope', [], acls='nope')


@pytest.mark.vcr()
def test_targetgroups_create_members_unexpectedvalue(api):
    '''
    test to raise the exception when value of members is not as defined
    '''
    with pytest.raises(UnexpectedValueError):
        api.target_groups.create('nope', [])


@pytest.mark.vcr()
def test_targetgroups_create(api, targetgroup):
    '''
    test to create the targetgroups
    '''
    assert isinstance(targetgroup, dict)
    check(targetgroup, 'acls', list)
    for data in targetgroup['acls']:
        check(data, 'display_name', str, allow_none=True)
        check(data, 'id', int, allow_none=True)
        check(data, 'name', str, allow_none=True)
        check(data, 'owner', int, allow_none=True)
        check(data, 'permissions', int)
        check(data, 'type', str)
    check(targetgroup, 'creation_date', int)
    check(targetgroup, 'default_group', int)
    check(targetgroup, 'id', int)
    check(targetgroup, 'last_modification_date', int)
    check(targetgroup, 'members', str)
    check(targetgroup, 'name', str)
    check(targetgroup, 'owner', str)
    check(targetgroup, 'owner_id', int)
    check(targetgroup, 'shared', int)
    check(targetgroup, 'user_permissions', int)


@pytest.mark.vcr()
def test_targetgroups_delete_id_typeerror(api):
    '''
    test to raise the exception when the type of target group
    to be deleted is not as defined
    '''
    with pytest.raises(TypeError):
        api.target_groups.delete('nope')


@pytest.mark.vcr()
def test_targetgroups_delete(api, targetgroup):
    '''
    test to delete the target group
    '''
    pass


@pytest.mark.vcr()
def test_targetgroups_details_id_typeerror(api):
    '''
    test to raise the exception when type of id is not as defined
    '''
    with pytest.raises(TypeError):
        api.target_groups.details('nope')


@pytest.mark.vcr()
def test_targetgroups_details(api, targetgroup):
    '''
    test to get the target groups details
    '''
    group = api.target_groups.details(targetgroup['id'])
    assert isinstance(group, dict)
    assert group['id'] == targetgroup['id']
    check(group, 'acls', list)
    for data in group['acls']:
        check(data, 'display_name', str, allow_none=True)
        check(data, 'id', int, allow_none=True)
        check(data, 'name', str, allow_none=True)
        check(data, 'owner', int, allow_none=True)
        check(data, 'permissions', int)
        check(data, 'type', str)
    check(group, 'creation_date', int)
    check(group, 'default_group', int)
    check(group, 'id', int)
    check(group, 'last_modification_date', int)
    check(group, 'members', str)
    check(group, 'name', str)
    check(group, 'owner', str)
    check(group, 'owner_id', int)
    check(group, 'shared', int)
    check(group, 'user_permissions', int)


@pytest.mark.vcr()
def test_targetgroups_edit_id_typeerror(api):
    '''
    test to raise the exception when type of id is not as defined
    '''
    with pytest.raises(TypeError):
        api.target_groups.delete('nope')


@pytest.mark.vcr()
def test_targetgroups_edit_name_typeerror(api):
    '''
    test to raise the exception when type of name is not as defined
    '''
    with pytest.raises(TypeError):
        api.target_groups.edit(1, 1)


@pytest.mark.vcr()
def test_targetgroups_edit_acls_typeerror(api):
    '''
    test to raise the exception when type of acls is not as defined
    '''
    with pytest.raises(TypeError):
        api.target_groups.edit(1, acls=False)


@pytest.mark.vcr()
def test_targetgroups_edit(api, targetgroup):
    '''
    test to edit the target groups
    '''
    members = targetgroup['members'].split(',')
    members.append('192.168.0.2')
    resp = api.target_groups.edit(targetgroup['id'], members=members)
    assert isinstance(resp, dict)
    check(resp, 'acls', list)
    for data in resp['acls']:
        check(data, 'display_name', str, allow_none=True)
        check(data, 'id', int, allow_none=True)
        check(data, 'name', str, allow_none=True)
        check(data, 'owner', int, allow_none=True)
        check(data, 'permissions', int)
        check(data, 'type', str)
    check(resp, 'creation_date', int)
    check(resp, 'default_group', int)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'owner', str)
    check(resp, 'owner_id', int)
    check(resp, 'shared', int)
    check(resp, 'user_permissions', int)
    assert resp['members'] == ', '.join(members)


@pytest.mark.vcr()
def test_targetgroups_list(api):
    '''
    test to verify the types of target groups list
    '''
    assert isinstance(api.target_groups.list(), list)


@pytest.mark.vcr()
def test_targetgroups_edit_fields(api, targetgroup):
    """
    test to edit the target groups
    """
    members = targetgroup['members'].split(',')
    members.append('192.168.0.2')
    resp = api.target_groups.edit(targetgroup['id'], members=members, name='targetgroup_name')
    assert isinstance(resp, dict)
    check(resp, 'acls', list)
    for data in resp['acls']:
        check(data, 'display_name', str, allow_none=True)
        check(data, 'id', int, allow_none=True)
        check(data, 'name', str, allow_none=True)
        check(data, 'owner', int, allow_none=True)
        check(data, 'permissions', int)
        check(data, 'type', str)
    check(resp, 'creation_date', int)
    check(resp, 'default_group', int)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'owner', str)
    check(resp, 'owner_id', int)
    check(resp, 'shared', int)
    check(resp, 'user_permissions', int)
    assert resp['members'] == ', '.join(members)
