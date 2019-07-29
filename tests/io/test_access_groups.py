from tenable.errors import *
from ..checker import check, single
import pytest, uuid

@pytest.fixture
def rules():
    return [('ipv4', 'eq', ['192.168.0.0/24'])]

@pytest.fixture
def agroup(request, api, vcr, rules):
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
    with pytest.raises(TypeError):
        api.access_groups._principal_constructor([(1, 'something')])

def test_access_group_principal_constructor_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups._principal_constructor([('something', 'something')])

def test_access_group_principal_constructor_id_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups._principal_constructor([('user', 1)])

def test_access_group_principal_constructor_dict_type_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups._principal_constructor([{
            'type': 1,
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])

def test_access_group_principal_constructor_dict_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups._principal_constructor([{
            'type': 'something',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])

def test_access_group_principal_constructor_dict_id_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups._principal_constructor([{
            'type': 'user',
            'principal_id': 1,
            'principal_name': 'test@test.com'
        }])

def test_access_group_principal_constructor_dict_name_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups._principal_constructor([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 1
        }])

def test_access_group_principal_constructor_tuple_pass(api):
    assert api.access_groups._principal_constructor([
        ('user', 'test@test.com')
    ]) == [{'type': 'user', 'principal_name': 'test@test.com'}]

    u = str(uuid.uuid4())
    assert api.access_groups._principal_constructor([
        ('user', u)
    ]) == [{'type': 'user', 'principal_id': u}]

def test_access_group_principal_constructor_dict_pass(api):
    assert api.access_groups._principal_constructor([
        {'type': 'user', 'principal_name': 'test@test.com'}
    ]) == [{'type': 'user', 'principal_name': 'test@test.com'}]

    u = str(uuid.uuid4())
    assert api.access_groups._principal_constructor([
        {'type': 'user', 'principal_id': u}
    ]) == [{'type': 'user', 'principal_id': u}]

@pytest.mark.vcr()
def test_access_groups_create_name_typeerror(api, rules):
    with pytest.raises(TypeError):
        api.access_groups.create(1, rules)

@pytest.mark.vcr()
def test_access_groups_create_all_users_typeerror(api, rules):
    with pytest.raises(TypeError):
        api.access_groups.create('Test', rules, all_users='nope')

@pytest.mark.vcr()
def test_access_groups_create_success(api, agroup):
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
    api.access_groups.delete(agroup['id'])

@pytest.mark.vcr()
def test_access_group_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.edit(1)

@pytest.mark.vcr()
def test_access_group_edit_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups.edit('something')

@pytest.mark.vcr()
def test_access_group_edit_success(api, agroup):
    g = api.access_groups.edit(agroup['id'], name='Updated')
    assert isinstance(g, dict)
    check(g, 'created_at', 'datetime')
    check(g, 'updated_at', 'datetime')
    check(g, 'id', 'uuid')
    check(g, 'name', str)
    check(g, 'all_assets', bool)
    check(g, 'all_users', bool)
    check(g, 'rules', list)
    for rule in g['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    check(g, 'principals', list)
    for principal in agroup['principals']:
        check(principal, 'type', str)
        check(principal, 'principal_id', 'uuid')
        check(principal, 'principal_name', str)
    check(g, 'created_by_uuid', 'uuid')
    check(g, 'updated_by_uuid', 'uuid')
    check(g, 'created_by_name', str)
    check(g, 'updated_by_name', str)
    check(g, 'processing_percent_complete', int)

@pytest.mark.vcr()
def test_access_groups_details_success(api, agroup):
    g = api.access_groups.details(agroup['id'])
    assert isinstance(g, dict)
    check(g, 'created_at', 'datetime')
    check(g, 'updated_at', 'datetime')
    check(g, 'id', 'uuid')
    check(g, 'name', str)
    check(g, 'all_assets', bool)
    check(g, 'all_users', bool)
    check(g, 'rules', list)
    for rule in g['rules']:
        check(rule, 'type', str)
        check(rule, 'operator', str)
        check(rule, 'terms', list)
    check(g, 'principals', list)
    for principal in agroup['principals']:
        check(principal, 'type', str)
        check(principal, 'principal_id', 'uuid')
        check(principal, 'principal_name', str)
    check(g, 'created_by_uuid', 'uuid')
    check(g, 'updated_by_uuid', 'uuid')
    check(g, 'created_by_name', str)
    check(g, 'updated_by_name', str)
    check(g, 'processing_percent_complete', int)

@pytest.mark.vcr()
def test_access_groups_list_offset_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(offset='nope')

@pytest.mark.vcr()
def test_access_groups_list_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(limit='nope')

@pytest.mark.vcr()
def test_access_groups_list_sort_field_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(sort=((1, 'asc'),))

@pytest.mark.vcr()
def test_access_groups_list_sort_direction_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(sort=(('uuid', 1),))

@pytest.mark.vcr()
def test_access_groups_list_sort_direction_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups.list(sort=(('uuid', 'nope'),))

@pytest.mark.vcr()
def test_access_groups_list_filter_name_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list((1, 'match', 'win'))

@pytest.mark.vcr()
def test_access_groups_list_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(('name', 1, 'win'))

@pytest.mark.vcr()
def test_access_groups_list_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(('name', 'match', 1))

@pytest.mark.vcr()
def test_access_groups_list_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(filter_type=1)

@pytest.mark.vcr()
def test_access_groups_list_wildcard_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(wildcard=1)

@pytest.mark.vcr()
def test_access_groups_list_wildcard_fields_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups.list(wildcard_fields='nope')

@pytest.mark.vcr()
def test_access_groups_list(api):
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
        #check(i, 'created_by_uuid', 'uuid') # Will not return for default group
        check(i, 'updated_by_uuid', 'uuid')
        check(i, 'created_by_name', str)
        check(i, 'updated_by_name', str)
        check(i, 'processing_percent_complete', int)
        check(i, 'status', str)
    assert count == access_groups.total