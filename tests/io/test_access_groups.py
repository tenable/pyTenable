'''
test access_groups
'''
import uuid
import pytest
from tenable.errors import UnexpectedValueError, APIError
from tests.checker import check

@pytest.fixture(name='rules')
def fixture_rules():
    '''
    Fixture to return access_group rules structure
    '''
    return [('ipv4', 'eq', ['192.168.0.0/24'])]

@pytest.fixture(name='agroup')
def fixture_agroup(request, api, rules):
    '''
    Fixture to create access_group
    '''
    group = api.access_groups.create('Example', rules)
    def teardown():
        '''
        cleanup function to delete access_group
        '''
        try:
            api.access_groups.delete(group['id'])
        except APIError:
            pass

    request.addfinalizer(teardown)
    return group


def test_access_group_principal_constructor_type_typeerror(api):
    '''
    test to raise exception when type of type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([(1, 'something')])

def test_access_group_principal_constructor_type_unexpectedvalueerror(api):
    '''
    test to raise exception when type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups, '_principal_constructor')([('something', 'something')])

def test_access_group_principal_constructor_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([('user', 1)])

def test_access_group_principal_constructor_dict_type_typeerror(api):
    '''
    test to raise exception when type of type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 1,
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])


def test_access_group_principal_constructor_dict_type_unexpectedvalueerror(api):
    '''
    test to raise exception when type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 'something',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])


def test_access_group_principal_constructor_dict_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 'user',
            'principal_id': 1,
            'principal_name': 'test@test.com'
        }])


def test_access_group_principal_constructor_dict_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 1
        }])


def test_access_group_principal_constructor_tuple_pass(api):
    '''
    test to parse tuple type principals
    '''
    assert getattr(api.access_groups, '_principal_constructor')([
        ('user', 'test@test.com')
    ]) == [{'type': 'user', 'principal_name': 'test@test.com'}]

    user = str(uuid.uuid4())
    assert getattr(api.access_groups, '_principal_constructor')([
        ('user', user)
    ]) == [{'type': 'user', 'principal_id': user}]

def test_access_group_principal_constructor_dict_pass(api):
    '''
    test to parse dict type principals
    '''
    assert getattr(api.access_groups, '_principal_constructor')([
        {'type': 'user', 'principal_name': 'test@test.com'}
    ]) == [{'type': 'user', 'principal_name': 'test@test.com'}]

    user = str(uuid.uuid4())
    assert getattr(api.access_groups, '_principal_constructor')([
        {'type': 'user', 'principal_id': user}
    ]) == [{'type': 'user', 'principal_id': user}]

@pytest.mark.vcr()
def test_access_groups_create_name_typeerror(api, rules):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.create(1, rules)


@pytest.mark.vcr()
def test_access_groups_create_all_users_typeerror(api, rules):
    '''
    test to raise exception when type of all_users param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.create('Test', rules, all_users='nope')


@pytest.mark.vcr()
def test_access_groups_create_success(agroup):
    '''
   test to create access group
   '''
    assert isinstance(agroup, dict)
    check(agroup, 'created_at', 'datetime')
    check(agroup, 'updated_at', 'datetime')
    check(agroup, 'id', 'uuid')
    check(agroup, 'name', str)
    check(agroup, 'all_assets', bool)
    check(agroup, 'all_users', bool)
    check(agroup, 'rules', list)
    for rule in agroup['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    if 'principals' in agroup and agroup['principals']:
        check(agroup, 'principals', list)
        for principal in agroup['principals']:
            check(principal, 'type', str)
            check(principal, 'principal_id', 'uuid')
            check(principal, 'principal_name', str)
    check(agroup, 'created_by_uuid', 'uuid')
    check(agroup, 'updated_by_uuid', 'uuid')
    check(agroup, 'created_by_name', str)
    check(agroup, 'updated_by_name', str)
    check(agroup, 'processing_percent_complete', int)


@pytest.mark.vcr()
def test_access_groups_delete_success(api, agroup):
    '''
    test to delete access group
    '''
    api.access_groups.delete(agroup['id'])


@pytest.mark.vcr()
def test_access_group_edit_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.edit(1)


@pytest.mark.vcr()
def test_access_group_edit_id_unexpectedvalueerror(api):
    '''
    test to raise exception when group_id param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.access_groups.edit('something')


@pytest.mark.vcr()
def test_access_group_edit_success(api, agroup):
    '''
    test to edit access group
    '''
    group = api.access_groups.edit(agroup['id'], name='Updated')
    assert isinstance(group, dict)
    check(group, 'created_at', 'datetime')
    check(group, 'updated_at', 'datetime')
    check(group, 'id', 'uuid')
    check(group, 'name', str)
    check(group, 'all_assets', bool)
    check(group, 'all_users', bool)
    check(group, 'rules', list)
    for rule in group['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    if 'principals' in group and group['principals']:
        check(group, 'principals', list)
        for principal in group['principals']:
            check(principal, 'type', str)
            check(principal, 'principal_id', 'uuid')
            check(principal, 'principal_name', str)
    check(group, 'created_by_uuid', 'uuid')
    check(group, 'updated_by_uuid', 'uuid')
    check(group, 'created_by_name', str)
    check(group, 'updated_by_name', str)
    check(group, 'processing_percent_complete', int)

@pytest.mark.vcr()
def test_access_groups_details_success(api, agroup):
    '''
    test to get details of specific access group
    '''
    group = api.access_groups.details(agroup['id'])
    assert isinstance(group, dict)
    check(group, 'created_at', 'datetime')
    check(group, 'updated_at', 'datetime')
    check(group, 'id', 'uuid')
    check(group, 'name', str)
    check(group, 'all_assets', bool)
    check(group, 'all_users', bool)
    check(group, 'rules', list)
    for rule in group['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    if 'principals' in group and group['principals']:
        check(group, 'principals', list)
        for principal in group['principals']:
            check(principal, 'type', str)
            check(principal, 'principal_id', 'uuid')
            check(principal, 'principal_name', str)
    check(group, 'created_by_uuid', 'uuid')
    check(group, 'updated_by_uuid', 'uuid')
    check(group, 'created_by_name', str)
    check(group, 'updated_by_name', str)
    check(group, 'processing_percent_complete', int)

@pytest.mark.vcr()
def test_access_groups_list_offset_typeerror(api):
    '''
    test to raise exception when type of offset param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(offset='nope')


@pytest.mark.vcr()
def test_access_groups_list_limit_typeerror(api):
    '''
    test to raise exception when type of limit param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(limit='nope')


@pytest.mark.vcr()
def test_access_groups_list_sort_field_typeerror(api):
    '''
    test to raise exception when type of sort field_name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(sort=((1, 'asc'),))


@pytest.mark.vcr()
def test_access_groups_list_sort_direction_typeerror(api):
    '''
    test to raise exception when type of sort field_direction param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(sort=(('uuid', 1),))


@pytest.mark.vcr()
def test_access_groups_list_sort_direction_unexpectedvalue(api):
    '''
    test to raise exception when sort_firection param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.access_groups.list(sort=(('uuid', 'nope'),))


@pytest.mark.vcr()
def test_access_groups_list_filter_name_typeerror(api):
    '''
    test to raise exception when type of filter_name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list((1, 'match', 'win'))


@pytest.mark.vcr()
def test_access_groups_list_filter_operator_typeerror(api):
    '''
    test to raise exception when type of filter_operator param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(('name', 1, 'win'))


@pytest.mark.vcr()
def test_access_groups_list_filter_value_typeerror(api):
    '''
    test to raise exception when type of filter_value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(('name', 'match', 1))


@pytest.mark.vcr()
def test_access_groups_list_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(filter_type=1)


@pytest.mark.vcr()
def test_access_groups_list_wildcard_typeerror(api):
    '''
    test to raise exception when type of wildcard param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(wildcard=1)


@pytest.mark.vcr()
def test_access_groups_list_wildcard_fields_typeerror(api):
    '''
    test to raise exception when type of wildcard_fields param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(wildcard_fields='nope')


@pytest.mark.vcr()
def test_access_groups_list(api):
    '''
    test to get list of access groups
    '''
    count = 0
    access_groups = api.access_groups.list()
    for group in access_groups:
        count += 1
        assert isinstance(group, dict)
        check(group, 'created_at', 'datetime')
        check(group, 'updated_at', 'datetime')
        check(group, 'id', 'uuid')
        check(group, 'name', str)
        check(group, 'all_assets', bool)
        check(group, 'all_users', bool)
        #check(group, 'created_by_uuid', 'uuid') # Will not return for default group
        check(group, 'updated_by_uuid', 'uuid')
        check(group, 'created_by_name', str)
        check(group, 'updated_by_name', str)
        check(group, 'processing_percent_complete', int)
        check(group, 'status', str)
    assert count == access_groups.total

@pytest.mark.vcr()
def test_access_groups_list_fields(api):
    '''
    test to raise the exception to list the access groups
    '''
    count = 0
    access_groups = api.access_groups.list(filter_type='or',
                                           limit=45,
                                           offset=2,
                                           wildcard='match',
                                           wildcard_fields=['name'])
    for group in access_groups:
        count += 1
        assert isinstance(group, dict)
        check(group, 'created_at', 'datetime')
        check(group, 'updated_at', 'datetime')
        check(group, 'id', 'uuid')
        check(group, 'name', str)
        check(group, 'all_assets', bool)
        check(group, 'all_users', bool)
        # check(i, 'created_by_uuid', 'uuid') # Will not return for default group
        check(group, 'updated_by_uuid', 'uuid')
        check(group, 'created_by_name', str)
        check(group, 'updated_by_name', str)
        check(group, 'processing_percent_complete', int)
        check(group, 'status', str)
    assert count == access_groups.total
