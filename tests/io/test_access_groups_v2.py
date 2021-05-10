from tenable.errors import *
from ..checker import check, single
import pytest, uuid

@pytest.fixture
def rules():
    return [('ipv4', 'eq', ['192.168.0.0/24'])]

@pytest.fixture
def agroup(request, api, vcr, rules):
    with vcr.use_cassette('test_access_groups_v2_create_success'):
        group = api.access_groups_v2.create('Example', rules)
    def teardown():
        try:
            with vcr.use_cassette('test_access_groups_v2_delete_success'):
                api.access_groups_v2.delete(group['id'])
        except APIError:
            pass
    request.addfinalizer(teardown)
    return group

def test_access_group_v2_principal_constructor_type_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._principal_constructor([(1, 'something')])

def test_access_group_v2_principal_constructor_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2._principal_constructor([('something', 'something')])

def test_access_group_v2_principal_constructor_id_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._principal_constructor([('user', 1)])

def test_access_group_v2_principal_constructor_permission_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._principal_constructor([('user', str(uuid.uuid4()), 1)])

def test_access_group_v2_principal_constructor_permission_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2._principal_constructor([('user', str(uuid.uuid4()), ['nope'])])

def test_access_group_v2_principal_constructor_dict_type_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._principal_constructor([{
            'type': 1,
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])

def test_access_group_v2_principal_constructor_dict_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2._principal_constructor([{
            'type': 'something',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 'test@test.com'
        }])

def test_access_group_v2_principal_constructor_dict_id_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._principal_constructor([{
            'type': 'user',
            'principal_id': 1,
            'principal_name': 'test@test.com'
        }])

def test_access_group_v2_principal_constructor_dict_name_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._principal_constructor([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'principal_name': 1
        }])

def test_access_group_v2_principal_constructor_dict_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._principal_constructor([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'permissions': 1
        }])

def test_access_group_v2_principal_constructor_dict_permissions_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2._principal_constructor([{
            'type': 'user',
            'principal_id': str(uuid.uuid4()),
            'permissions': ['Nothing']
        }])

def test_access_group_v2_principal_constructor_tuple_pass(api):
    assert api.access_groups_v2._principal_constructor([
        ('user', 'test@test.com', ['can_view'])
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_name': 'test@test.com'}]

    u = str(uuid.uuid4())
    assert api.access_groups_v2._principal_constructor([
        ('user', u)
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_id': u}]

def test_access_group_v2_principal_constructor_dict_pass(api):
    assert api.access_groups_v2._principal_constructor([
        {'type': 'user', 'principal_name': 'test@test.com', 'permissions': ['CAN_VIEW']}
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_name': 'test@test.com'}]

    u = str(uuid.uuid4())
    assert api.access_groups_v2._principal_constructor([
        {'type': 'user', 'principal_id': u}
    ]) == [{'permissions': ['CAN_VIEW'], 'type': 'user', 'principal_id': u}]

def test_access_group_v2_list_clean_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2._list_clean(items='nope')

def test_access_group_v2_list_clean_pass(api):
    resp = api.access_groups_v2._list_clean(['one', 'two', 'one'])
    assert sorted(resp) == ['one', 'two']

@pytest.mark.vcr()
def test_access_groups_v2_create_name_typeerror(api, rules):
    with pytest.raises(TypeError):
        api.access_groups_v2.create(1, rules)

@pytest.mark.vcr()
def test_access_groups_v2_create_all_users_typeerror(api, rules):
    with pytest.raises(TypeError):
        api.access_groups_v2.create('Test', rules, all_users='nope')

@pytest.mark.vcr()
def test_access_groups_v2_create_access_group_type_typeerror(api, rules):
    with pytest.raises(TypeError):
        api.access_groups_v2.create('Test', rules, access_group_type=1)

@pytest.mark.vcr()
def test_access_groups_v2_create_access_group_type_unexpectedvalueerror(api, rules):
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2.create('Test', rules, access_group_type='nope')

@pytest.mark.vcr()
def test_access_groups_v2_create_principals_typeerror(api, rules):
    with pytest.raises(TypeError):
        api.access_groups_v2.create('Test', rules, principals='nope')

@pytest.mark.vcr()
def test_access_groups_v2_create_success(api, agroup):
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
    api.access_groups_v2.delete(agroup['id'])

@pytest.mark.vcr()
def test_access_groups_v2_list_offset_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(offset='nope')

@pytest.mark.vcr()
def test_access_groups_v2_list_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(limit='nope')

@pytest.mark.vcr()
def test_access_groups_v2_list_sort_field_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(sort=((1, 'asc'),))

@pytest.mark.vcr()
def test_access_groups_v2_list_sort_direction_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(sort=(('uuid', 1),))

@pytest.mark.vcr()
def test_access_groups_v2_list_sort_direction_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2.list(sort=(('uuid', 'nope'),))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_name_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list((1, 'match', 'win'))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(('name', 1, 'win'))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(('name', 'match', 1))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(filter_type=1)

@pytest.mark.vcr()
def test_access_groups_v2_list_wildcard_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(wildcard=1)

@pytest.mark.vcr()
def test_access_groups_v2_list_wildcard_fields_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(wildcard_fields='nope')

@pytest.mark.vcr()
def test_access_groups_v2_list(api):
    count = 0
    access_groups = api.access_groups_v2.list()
    for i in access_groups:
        count += 1
        assert isinstance(i, dict)
        check(i, 'created_at', 'datetime')
        check(i, 'updated_at', 'datetime')
        check(i, 'id', 'uuid')
        check(i, 'name', str)
        check(i, 'all_assets', bool)
        check(i, 'version', int)
        check(i, 'status', str)
        check(i, 'access_group_type', str)
        #check(i, 'created_by_uuid', 'uuid') # Will not return for default group
        #check(i, 'updated_by_uuid', 'uuid') # Will not return for default group
        check(i, 'created_by_name', str)
        check(i, 'updated_by_name', str)
        check(i, 'processing_percent_complete', int)
    assert count == access_groups.total
