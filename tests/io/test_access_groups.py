'''
test access groups
'''
import uuid
import pytest
from tenable.errors import APIError, UnexpectedValueError
from ..checker import check

@pytest.fixture
def rules():
    '''
    rules fixture
    '''
    return [('ipv4', 'eq', ['192.168.0.0/24'])]


@pytest.fixture
def agroup(request, api, vcr, rules):
    '''
    access group fixture
    '''
    with vcr.use_cassette('test_access_groups_create_success'):
        group = api.access_groups.create('Example', rules)

    def teardown():
        try:
            with vcr.use_cassette('test_access_groups_delete_success'):
                api.access_groups.delete(group['id'])
        except APIError:
            pass

    request.addfinalizer(teardown)
    return group


def test_access_group_principal_constructor_type_typeerror(api):
    '''
    test to raise the exception when principal constructor type doesnt match the expected type
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([(1, 'something')])


def test_access_group_principal_constructor_type_unexpectedvalueerror(api):
    '''
    test to raise the exception when principal constructor type gets the value which isn't expected
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups, '_principal_constructor')([('something', 'something')])


def test_access_group_principal_constructor_id_typeerror(api):
    '''
    test to raise the exception when principal constructor
    gets the type of the id which isn't expected
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([('user', 1)])


def test_access_group_principal_constructor_dict_type_typeerror(api):
    '''
    test to raise the exception when principal constructor gets the type which isn't expected
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 1,
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])


def test_access_group_principal_constructor_dict_type_unexpectedvalueerror(api):
    '''
    test to raise the exception when principal constructor gets the value which isn't expected
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 'something',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])


def test_access_group_principal_constructor_dict_id_typeerror(api):
    '''
    test to raise the exception when type of id in the principal
    constructor is not matching with defined
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 'user',
            'principal_id': 1,
            'principal_name': 'test@test.com'
        }])


def test_access_group_principal_constructor_dict_name_typeerror(api):
    '''
    test to raise the exception when type of name in the principal
    constructor is not matching with defined
    '''
    with pytest.raises(TypeError):
        getattr(api.access_groups, '_principal_constructor')([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 1
        }])


def test_access_group_principal_constructor_tuple_pass(api):
    '''
test to raise the exception to check the type of principal constructor
    '''
    resp = getattr(api.access_groups, '_principal_constructor')([('user', 'test@test.com')])
    assert resp == [{'type': 'user', 'principal_name': 'test@test.com'}]

    uuids = str(uuid.uuid4())
    resp = getattr(api.access_groups, '_principal_constructor')([('user', uuids)])
    assert resp == [{'type': 'user', 'principal_id': uuids}]


def test_access_group_principal_constructor_dict_pass(api):
    '''
test to raise the exception to check the type of principal constructor
    '''
    resp = getattr(api.access_groups, '_principal_constructor')([
        {'type': 'user', 'principal_name': 'test@test.com'}
    ])
    assert resp == [{'type': 'user', 'principal_name': 'test@test.com'}]

    uuids = str(uuid.uuid4())
    resp = getattr(api.access_groups, '_principal_constructor')\
        ([{'type': 'user', 'principal_id': uuids}])
    assert resp == [{'type': 'user', 'principal_id': uuids}]


@pytest.mark.vcr()
def test_access_groups_create_name_typeerror(api, rules):
    '''
    test to raise the exception when type of name is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.create(1, rules)


@pytest.mark.vcr()
def test_access_groups_create_all_users_typeerror(api, rules):
    '''
    test to raise the exception when type of argument
    in create is not matching with the desired type
    '''
    with pytest.raises(TypeError):
        api.access_groups.create('Test', rules, all_users='nope')


@pytest.mark.vcr()
def test_access_groups_create_success(agroup):
    '''
    test to create the access group
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
    test to delete the access group
    '''
    api.access_groups.delete(agroup['id'])


@pytest.mark.vcr()
def test_access_group_edit_id_typeerror(api):
    '''
    test to raise the exception when type of access group id is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.edit(1)


@pytest.mark.vcr()
def test_access_group_edit_id_unexpectedvalueerror(api):
    '''
    test to check raise the exception when access group id gets the non defined value
    '''
    with pytest.raises(UnexpectedValueError):
        api.access_groups.edit('something')


@pytest.mark.vcr()
def test_access_group_edit_success(api, agroup):
    '''
    test to edit the access group and verifying their types
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
    check(group, 'principals', list)
    for principal in agroup['principals']:
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
    test to check the details of the access group and verifying their types
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
    check(group, 'principals', list)
    for principal in agroup['principals']:
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
    test to raise the exception when type of limit name is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(offset='nope')


@pytest.mark.vcr()
def test_access_groups_list_limit_typeerror(api):
    '''
    test to raise the exception when type of limit is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(limit='nope')


@pytest.mark.vcr()
def test_access_groups_list_sort_field_typeerror(api):
    '''
    test to raise the exception when type of sorting field is not as defined
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(sort=((1, 'asc'),))


@pytest.mark.vcr()
def test_access_groups_list_sort_direction_typeerror(api):
    '''

test to raise the exception when sort param doesnt get the expected type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(sort=(('uuid', 1),))


@pytest.mark.vcr()
def test_access_groups_list_sort_direction_unexpectedvalue(api):
    '''
    test to raise the exception when sort param doesnt get the expected value
    '''
    with pytest.raises(UnexpectedValueError):
        api.access_groups.list(sort=(('uuid', 'nope'),))


@pytest.mark.vcr()
def test_access_groups_list_filter_name_typeerror(api):
    '''
    test to raise the exception when type of filter name is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list((1, 'match', 'win'))


@pytest.mark.vcr()
def test_access_groups_list_filter_operator_typeerror(api):
    '''
    test to raise the exception when type of filter is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(('name', 1, 'win'))


@pytest.mark.vcr()
def test_access_groups_list_filter_value_typeerror(api):
    '''

    test to raise the exception when type of filter_value is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(('name', 'match', 1))


@pytest.mark.vcr()
def test_access_groups_list_filter_type_typeerror(api):
    '''
    test to raise the exception when type of filter_type is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(filter_type=1)


@pytest.mark.vcr()
def test_access_groups_list_wildcard_typeerror(api):
    '''
    test to raise the exception when type of wildcard is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(wildcard=1)


@pytest.mark.vcr()
def test_access_groups_list_wildcard_fields_typeerror(api):
    '''
    test to raise the exception when type of wildcard fields is not matching with the defined type
    '''
    with pytest.raises(TypeError):
        api.access_groups.list(wildcard_fields='nope')


@pytest.mark.vcr()
def test_access_groups_list(api):
    '''
    test to raise the exception to list the access groups
    '''
    count = 0
    access_groups = api.access_groups.list()
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
