'''
test access_groups
'''
import uuid
import pytest
from tenable.errors import UnexpectedValueError, APIError
from tests.checker import check
from tests.io.test_groups import fixture_group

@pytest.fixture(name='rules')
def fixture_rules():
    '''
    Fixture to return access_group rules structure
    '''
    return [('ipv4', 'eq', ['192.168.0.0/24'])]


@pytest.fixture(name='agroup')
def fixture_agroup(request, api, vcr, rules):
    '''
    Fixture to create access_group
    '''
    with vcr.use_cassette('test_access_groups_v2_create_success'):
        group = api.access_groups_v2.create('Example', rules)

    def teardown():
        '''
        cleanup function to delete access_group
        '''
        try:
            with vcr.use_cassette('test_access_groups_v2_delete_success'):
                api.access_groups_v2.delete(group['id'])
        except APIError:
            pass

    request.addfinalizer(teardown)
    return group


def test_access_group_v2_principal_constructor_type_typeerror(api):
    '''
    test to raise exception when type of type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_principal_constructor')([(1, 'something')])


def test_access_group_v2_principal_constructor_type_unexpectedvalueerror(api):
    '''
    test to raise exception when type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups_v2, '_principal_constructor')([('something', 'something')])


def test_access_group_v2_principal_constructor_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_principal_constructor')([('user', 1)])


def test_access_group_v2_principal_constructor_permission_typeerror(api):
    '''
    test to raise exception when type of permissions param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_principal_constructor')([('user', str(uuid.uuid4()), 1)])


def test_access_group_v2_principal_constructor_permission_unexpectedvalueerror(api):
    '''
    test to raise exception when permissions param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups_v2, '_principal_constructor')([
            ('user', str(uuid.uuid4()), ['nope'])])


def test_access_group_v2_principal_constructor_dict_type_typeerror(api):
    '''
    test to raise exception when type of type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_principal_constructor')([{
            'type': 1,
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])


def test_access_group_v2_principal_constructor_dict_type_unexpectedvalueerror(api):
    '''
    test to raise exception when type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups_v2, '_principal_constructor')([{
            'type': 'something',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])


def test_access_group_v2_principal_constructor_dict_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_principal_constructor')([{
            'type': 'user',
            'principal_id': 1,
            'principal_name': 'test@test.com'
        }])


def test_access_group_v2_principal_constructor_dict_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_principal_constructor')([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 1
        }])


def test_access_group_v2_principal_constructor_dict_permissions_typeerror(api):
    '''
    test to raise exception when type of permissions param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_principal_constructor')([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'permissions': 1
        }])


def test_access_group_v2_principal_constructor_dict_permissions_unexpectedvalueerror(api):
    '''
    test to raise exception when permissions param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups_v2, '_principal_constructor')([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'permissions': ['Nothing']
        }])


def test_access_group_v2_principal_constructor_tuple_pass(api):
    '''
    test to parse tuple type principals
    '''
    assert getattr(api.access_groups_v2, '_principal_constructor')([
        ('user', 'test@test.com', ['can_view'])
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_name': 'test@test.com'}]

    user_id = str(uuid.uuid4())
    assert getattr(api.access_groups_v2, '_principal_constructor')([
        ('user', user_id)
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_id': user_id}]


def test_access_group_v2_principal_constructor_dict_pass(api):
    '''
    test to parse dict type principals
    '''
    assert getattr(api.access_groups_v2, '_principal_constructor')([
        {'type': 'user', 'principal_name': 'test@test.com', 'permissions': ['CAN_VIEW']}
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_name': 'test@test.com'}]

    user_id = str(uuid.uuid4())
    assert getattr(api.access_groups_v2, '_principal_constructor')([
        {'type': 'user', 'principal_id': user_id}
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_id': user_id}]


def test_access_group_v2_list_clean_typeerror(api):
    '''
    test to raise exception when type of items param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups_v2, '_list_clean')(items='nope')


def test_access_group_v2_list_clean_pass(api):
    '''
    test to remove duplicates from list
    '''
    resp = getattr(api.access_groups_v2, '_list_clean')(['one', 'two', 'one'])
    assert sorted(resp) == ['one', 'two']


@pytest.mark.vcr()
def test_access_groups_v2_create_name_typeerror(api, rules):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.create(1, rules)


@pytest.mark.vcr()
def test_access_groups_v2_create_all_users_typeerror(api, rules):
    '''
    test to raise exception when type of all_users param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.create('Test', rules, all_users='nope')


@pytest.mark.vcr()
def test_access_groups_v2_create_access_group_type_typeerror(api, rules):
    '''
    test to raise exception when type of access_group_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.create('Test', rules, access_group_type=1)


@pytest.mark.vcr()
def test_access_groups_v2_create_access_group_type_unexpectedvalueerror(api, rules):
    '''
    test to raise exception when access_group_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2.create('Test', rules, access_group_type='nope')


@pytest.mark.vcr()
def test_access_groups_v2_create_principals_typeerror(api, rules):
    '''
    test to raise exception when type of principals param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.create('Test', rules, principals='nope')


@pytest.mark.vcr()
def test_access_groups_v2_create_success(agroup):
    '''
    test to create access group
    '''
    assert isinstance(agroup, dict)
    check(agroup, 'created_at', 'datetime')
    check(agroup, 'updated_at', 'datetime')
    check(agroup, 'id', 'uuid')
    check(agroup, 'name', str)
    check(agroup, 'all_assets', bool)
    check(agroup, 'version', int)
    check(agroup, 'status', str)
    check(agroup, 'access_group_type', str)
    check(agroup, 'rules', list)
    for rule in agroup['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    check(agroup, 'principals', list)
    for principal in agroup['principals']:
        check(principal, 'type', str)
        check(principal, 'principal_id', 'uuid')
        check(principal, 'principal_name', str)
        check(principal, 'permissions', list)
    check(agroup, 'created_by_uuid', 'uuid')
    check(agroup, 'updated_by_uuid', 'uuid')
    check(agroup, 'created_by_name', str)
    check(agroup, 'updated_by_name', str)
    check(agroup, 'processing_percent_complete', int)


@pytest.mark.vcr()
def test_access_groups_v2_delete_success(api, agroup):
    '''
    test to delete access group
    '''
    api.access_groups_v2.delete(agroup['id'])


@pytest.mark.vcr()
def test_access_group_v2_edit_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.edit(1)


@pytest.mark.vcr()
def test_access_group_v2_edit_id_unexpectedvalueerror(api):
    '''
    test to raise exception when group_id param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2.edit('something')


@pytest.mark.vcr()
def test_access_group_v2_edit_success(api, agroup):
    '''
    test to edit access group
    '''
    resp = api.access_groups_v2.edit(agroup['id'], name='Updated', all_users=False)
    assert isinstance(resp, dict)
    check(resp, 'created_at', 'datetime')
    check(resp, 'updated_at', 'datetime')
    check(resp, 'id', 'uuid')
    check(resp, 'name', str)
    check(resp, 'all_assets', bool)
    check(resp, 'version', int)
    check(resp, 'status', str)
    check(resp, 'access_group_type', str)
    check(resp, 'rules', list)
    for rule in resp['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    check(resp, 'principals', list)
    for principal in resp['principals']:
        check(principal, 'type', str)
        check(principal, 'principal_id', 'uuid')
        check(principal, 'principal_name', str)
        check(principal, 'permissions', list)
    check(resp, 'created_by_uuid', 'uuid')
    check(resp, 'updated_by_uuid', 'uuid')
    check(resp, 'created_by_name', str)
    check(resp, 'updated_by_name', str)
    check(resp, 'processing_percent_complete', int)


@pytest.mark.vcr()
def test_access_groups_v2_details_success(api):
    '''
    test to get details of specific access group
    '''
    group = api.access_groups_v2.create('Test', [('ipv4', 'eq', ['192.168.0.0/24'])])
    resp = api.access_groups_v2.details(group['id'])
    assert isinstance(resp, dict)
    check(resp, 'created_at', 'datetime')
    check(resp, 'updated_at', 'datetime')
    check(resp, 'id', 'uuid')
    check(resp, 'name', str)
    check(resp, 'all_assets', bool)
    check(resp, 'version', int)
    check(resp, 'status', str)
    check(resp, 'access_group_type', str)
    check(resp, 'rules', list)
    for rule in resp['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    check(resp, 'principals', list)
    for principal in group['principals']:
        check(principal, 'type', str)
        check(principal, 'principal_id', 'uuid')
        check(principal, 'principal_name', str)
        check(principal, 'permissions', list)
    check(resp, 'created_by_uuid', 'uuid')
    check(resp, 'updated_by_uuid', 'uuid')
    check(resp, 'created_by_name', str)
    check(resp, 'updated_by_name', str)
    check(resp, 'processing_percent_complete', int)
    api.access_groups_v2.delete(group['id'])


@pytest.mark.vcr()
def test_access_groups_v2_list_offset_typeerror(api):
    '''
    test to raise exception when type of offset param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(offset='nope')


@pytest.mark.vcr()
def test_access_groups_v2_list_limit_typeerror(api):
    '''
    test to raise exception when type of limit param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(limit='nope')


@pytest.mark.vcr()
def test_access_groups_v2_list_sort_field_typeerror(api):
    '''
    test to raise exception when type of sort field_name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(sort=((1, 'asc'),))


@pytest.mark.vcr()
def test_access_groups_v2_list_sort_direction_typeerror(api):
    '''
    test to raise exception when type of sort field_direction param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(sort=(('uuid', 1),))


@pytest.mark.vcr()
def test_access_groups_v2_list_sort_direction_unexpectedvalue(api):
    '''
    test to raise exception when sort_firection param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2.list(sort=(('uuid', 'nope'),))


@pytest.mark.vcr()
def test_access_groups_v2_list_filter_name_typeerror(api):
    '''
    test to raise exception when type of filter_name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list((1, 'match', 'win'))


@pytest.mark.vcr()
def test_access_groups_v2_list_filter_operator_typeerror(api):
    '''
    test to raise exception when type of filter_operator param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(('name', 1, 'win'))


@pytest.mark.vcr()
def test_access_groups_v2_list_filter_value_typeerror(api):
    '''
    test to raise exception when type of filter_value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(('name', 'match', 1))


@pytest.mark.vcr()
def test_access_groups_v2_list_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(filter_type=1)


@pytest.mark.vcr()
def test_access_groups_v2_list_wildcard_typeerror(api):
    '''
    test to raise exception when type of wildcard param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(wildcard=1)


@pytest.mark.vcr()
def test_access_groups_v2_list_wildcard_fields_typeerror(api):
    '''
    test to raise exception when type of wildcard_fields param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.access_groups_v2.list(wildcard_fields='nope')


@pytest.mark.vcr()
def test_access_groups_v2_list(api):
    '''
    test to get list of access groups
    '''
    count = 0
    access_groups = api.access_groups_v2.list()
    for group in access_groups:
        count += 1
        assert isinstance(group, dict)
        check(group, 'created_at', 'datetime')
        check(group, 'updated_at', 'datetime')
        check(group, 'id', 'uuid')
        check(group, 'name', str)
        check(group, 'all_assets', bool)
        check(group, 'version', int)
        check(group, 'status', str)
        check(group, 'access_group_type', str)
        # check(group, 'created_by_uuid', 'uuid') # Will not return for default group
        # check(group, 'updated_by_uuid', 'uuid') # Will not return for default group
        check(group, 'created_by_name', str)
        check(group, 'updated_by_name', str)
        check(group, 'processing_percent_complete', int)
    assert count == access_groups.total




@pytest.mark.vcr()
def test_access_groups_v2_list_fields(api):
    '''
    test to get the list of access groups v2 and to verify their types
    '''
    count = 0
    access_groups = api.access_groups_v2.list(filter_type='or',
                                           limit=45,
                                           offset=2,
                                           wildcard='match',
                                           wildcard_fields=['name'])
    for i in access_groups:
        count += 1
        assert isinstance(i, dict)
        check(i, 'created_at', 'datetime')
        check(i, 'updated_at', 'datetime')
        check(i, 'id', 'uuid')
        check(i, 'name', str)
        check(i, 'all_assets', bool)
        check(i, 'all_users', bool)
        # check(i, 'created_by_uuid', 'uuid') # Will not return for default group
        check(i, 'updated_by_uuid', 'uuid')
        check(i, 'created_by_name', str)
        check(i, 'updated_by_name', str)
        check(i, 'processing_percent_complete', int)
        check(i, 'status', str)
    assert count == access_groups.total
