from tenable.errors import *
from ..checker import check, single
import pytest, uuid

def test_credentials_permissions_constructor_tuple_permission_type_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials._permissions_constructor([
            (1, 32, str(uuid.uuid4()))])

def test_credentials_permissions_constructor_tuple_permission_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials._permissions_constructor([
            ('nope', 32, str(uuid.uuid4()))])

def test_credentials_permissions_constructor_tuple_permission_permission_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials._permissions_constructor([
            ('user', 256, str(uuid.uuid4()))])

def test_credentials_permissions_constructor_tuple_permission_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials._permissions_constructor([
            ('user', 32, 1)])

def test_credentials_permissions_constructor_tuple_permission_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials._permissions_constructor([
            ('user', 32, 'someone')])

def test_credentials_permissions_constructor_dict_permission_type_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials._permissions_constructor([{
            'type': 1,
            'permissions': 32,
            'grantee_uuid': str(uuid.uuid4())
        }])

def test_credentials_permissions_constructor_dict_permission_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials._permissions_constructor([{
            'type': 'nope',
            'permissions': 32,
            'grantee_uuid': str(uuid.uuid4())
        }])

def test_credentials_permissions_constructor_dict_permission_permission_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials._permissions_constructor([{
            'type': 'user',
            'permissions': 256,
            'grantee_uuid': str(uuid.uuid4())
        }])

def test_credentials_permissions_constructor_dict_permission_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials._permissions_constructor([{
            'type': 'user',
            'permissions': 32,
            'grantee_uuid': 1
        }])

def test_credentials_permissions_constructor_dict_permission_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials._permissions_constructor([{
            'type': 'user',
            'permissions': 32,
            'grantee_uuid': 'someone'
        }])

def test_credentials_permissions_constructor_tuple_success(api):
    test_id = str(uuid.uuid4())
    assert api.credentials._permissions_constructor([('user', 32, test_id)]) == [{
        'type': 'user',
        'permissions': 32,
        'grantee_uuid': test_id
    }]
    assert api.credentials._permissions_constructor([('user', 'use', test_id)]) == [{
        'type': 'user',
        'permissions': 32,
        'grantee_uuid': test_id
    }]

def test_credentials_permissions_constructor_dict_success(api):
    test_id = str(uuid.uuid4())
    assert api.credentials._permissions_constructor([{
        'type': 'user',
        'permissions': 32,
        'grantee_uuid': test_id
    }]) == [{
        'type': 'user',
        'permissions': 32,
        'grantee_uuid': test_id
    }]

@pytest.fixture
def cred(request, api, vcr):
    with vcr.use_cassette('test_credentials_create_success'):
        cred = api.credentials.create('Example Cred', 'SSH',
            username='root',
            password='something',
            auth_method='password',
            elevate_privileges_with='Nothing',
            custom_password_prompt='')
    def teardown():
        try:
            with vcr.use_cassette('test_credentials_delete_success'):
                api.credentials.delete(cred)
        except APIError:
            pass
    request.addfinalizer(teardown)
    return cred

def test_credentials_create_cred_name_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.create(1, 'something')

def test_credentials_create_cred_type_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.create('something', 1)

def test_credentials_create_description_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.create('something', 'something', 1)

@pytest.mark.vcr()
def test_credentials_create_success(api, cred):
    single(cred, 'uuid')

def test_credentials_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.delete(1)

def test_credentials_delete_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials.delete('something')

@pytest.mark.vcr()
def test_credentials_delete_success(api, cred):
    api.credentials.delete(cred)

def test_credentials_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.edit(1)

def test_credentials_edit_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials.edit('something')

@pytest.mark.vcr()
def test_credentials_edit_success(api, cred):
    c = api.credentials.edit(cred, cred_name='updated cred')
    assert isinstance(c, bool)

def test_credentials_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.details(1)

def test_credentials_details_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials.details('something')

@pytest.mark.vcr()
def test_credentials_details_success(api, cred):
    c = api.credentials.details(cred)
    assert isinstance(c, dict)
    check(c, 'name', str)
    check(c, 'description', str)
    check(c, 'category', dict)
    check(c['category'], 'id', str)
    check(c['category'], 'name', str)
    check(c, 'type', dict)
    check(c['type'], 'id', str)
    check(c['type'], 'name', str)
    check(c, 'ad_hoc', bool)
    check(c, 'user_permissions', int)
    check(c, 'settings', dict)
    for k in c['settings']:
        check(c['settings'], k, str)
    check(c, 'permissions', list)
    for p in c['permissions']:
        check(p, 'grantee_uuid', 'uuid')
        check(p, 'type', str)
        check(p, 'permissions', int)
        check(p, 'name', str)

@pytest.mark.vcr()
def test_credentials_list_offset_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(offset='nope')

@pytest.mark.vcr()
def test_credentials_list_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(limit='nope')

@pytest.mark.vcr()
def test_credentials_list_sort_field_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(sort=((1, 'asc'),))

@pytest.mark.vcr()
def test_credentials_list_sort_direction_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(sort=(('uuid', 1),))

@pytest.mark.vcr()
def test_credentials_list_sort_direction_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.credentials.list(sort=(('uuid', 'nope'),))

@pytest.mark.vcr()
def test_credentials_list_filter_name_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list((1, 'match', 'win'))

@pytest.mark.vcr()
def test_credentials_list_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(('name', 1, 'win'))

@pytest.mark.vcr()
def test_credentials_list_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(('name', 'match', 1))

@pytest.mark.vcr()
def test_credentials_list_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(filter_type=1)

@pytest.mark.vcr()
def test_credentials_list_wildcard_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(wildcard=1)

@pytest.mark.vcr()
def test_credentials_list_wildcard_fields_typeerror(api):
    with pytest.raises(TypeError):
        api.credentials.list(wildcard_fields='nope')

@pytest.mark.vcr()
def test_credentials_list(api):
    count = 0
    credentials = api.credentials.list()
    for c in credentials:
        count += 1
        assert isinstance(c, dict)
        check(c, 'uuid', str)
        check(c, 'name', str)
        check(c, 'description', str)
        check(c, 'category', dict)
        check(c['category'], 'id', str)
        check(c['category'], 'name', str)
        check(c, 'type', dict)
        check(c['type'], 'id', str)
        check(c['type'], 'name', str)
        check(c, 'created_date', int)
        check(c, 'created_by', dict)
        check(c['created_by'], 'id', int)
        check(c['created_by'], 'display_name', str)
        check(c, 'last_used_by', dict)
        check(c['last_used_by'], 'id', int, allow_none=True)
        check(c['last_used_by'], 'display_name', str, allow_none=True)
        check(c, 'permission', int)
        check(c, 'user_permissions', int)
    assert count == credentials.total