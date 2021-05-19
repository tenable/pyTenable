from ..checker import check, single
from tenable.errors import *
from tenable.io.tags import TagsIterator
import uuid, pytest

@pytest.fixture
def tagfilters():
    return [('ipv4', 'eq', ['192.168.0.0/24'])]

@pytest.fixture
def filterdefs():
     return {
        'ipv4': {'choices': None,
                 'operators': ['eq'],
                 'pattern': '^(\\s*((?=\\d+\\.\\d+\\.\\d+\\.\\d+(?:\\/|-|\\s*,|$))'
                            '(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})'
                            '(?:(?:\\/(?:3[0-2]|[12]+\\d|[1-9]))|((?:-(?=\\d+\\.\\d+\\.\\d+\\.\\d+)'
                            '(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})|(?:\\s*,(?:\\s*)))?)+)+$'},
    }

@pytest.fixture
@pytest.mark.vcr()
def tagvalue(request, api):
    tag = api.tags.create('Example', 'Test')
    def teardown():
        try:
            api.tags.delete(tag['uuid'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return tag

@pytest.fixture
@pytest.mark.vcr()
def tagcat(request, api):
    tag = api.tags.create_category('Example3')
    def teardown():
        try:
            api.tags.delete_category(tag['uuid'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return tag

def test_tags_permission_constructor_id_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([(1, 'something', 'user')])

def test_tags_permission_constructor_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._permission_constructor([('something', 'something', 'user')])

def test_tags_permission_constructor_name_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([(str(uuid.uuid4()), 1, 'user')])

def test_tags_permission_constructor_type_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([(str(uuid.uuid4()), 'something', 1)])

def test_tags_permission_constructor_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._permission_constructor([(str(uuid.uuid4()), 'something', 'something')])

def test_tags_permission_constructor_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([(str(uuid.uuid4()), 'something', 'user', 1)])

def test_tags_permission_constructor_permissions_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._permission_constructor([(str(uuid.uuid4()), 'something', 'user', ['something'])])

def test_tags_permission_constructor_dict_id_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([{
            'id': 1,
            "name": 'something',
            "type": 'something',
            "permissions": [],
        }])

def test_tags_permission_constructor_dict_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._permission_constructor([{
            'id': 'something',
            "name": 'something',
            "type": 'something',
            "permissions": [],
        }])

def test_tags_permission_constructor_dict_name_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([{
            'id': str(uuid.uuid4()),
            "name": 1,
            "type": 'something',
            "permissions": [],
        }])

def test_tags_permission_constructor_dict_type_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 1,
            "permissions": [],
        }])

def test_tags_permission_constructor_dict_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._permission_constructor([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 'something',
            "permissions": [],
        }])

def test_tags_permission_constructor_dict_permission_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._permission_constructor([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 'user',
            "permissions": 1,
        }])

def test_tags_permission_constructor_dict_permission_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._permission_constructor([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 'user',
            "permissions": ['something'],
        }])

def test_tags_permission_constructor_tuple_pass(api):
    u = str(uuid.uuid4())
    assert api.tags._permission_constructor([
        (u, 'test', 'user', ['CAN_EDIT'])
    ]) == [{'permissions': ['CAN_EDIT'], 'type': 'USER', 'name': 'test', 'id': u}]

    # when permissions not passed
    assert api.tags._permission_constructor([
        (u, 'test', 'user')
    ]) == [{'permissions': [], 'type': 'USER', 'name': 'test', 'id': u}]

def test_tags_permission_constructor_dict_pass(api):
    u = str(uuid.uuid4())
    assert api.tags._permission_constructor([
        {'id': u, 'name': 'test', 'type': 'user', 'permissions': ['CAN_EDIT']}
    ]) == [{'permissions': ['CAN_EDIT'], 'type': 'USER', 'name': 'test', 'id': u}]

    # when permissions not passed
    assert api.tags._permission_constructor([
        {'id': u, 'name': 'test', 'type': 'user'}
    ]) == [{'permissions': [], 'type': 'USER', 'name': 'test', 'id': u}]

def test_tags_tag_value_constructor_filter_type_typeerror(api, tagfilters, filterdefs):
    with pytest.raises(TypeError):
        api.tags._tag_value_constructor(filters=tagfilters, filterdefs=filterdefs, filter_type=1)

def test_tags_tag_value_constructor_filter_type_unexpectedvalueerror(api, tagfilters, filterdefs):
    with pytest.raises(UnexpectedValueError):
        api.tags._tag_value_constructor(filters=tagfilters, filterdefs=filterdefs, filter_type='nope')

def test_tags_tag_value_constructor_pass(api, tagfilters, filterdefs):
    assert api.tags._tag_value_constructor(
        filters=tagfilters, filterdefs=filterdefs, filter_type='and'
    ) == {'asset': {'and': [{'field': 'ipv4', 'operator': 'eq', 'value': '192.168.0.0/24'}]}}

@pytest.mark.vcr()
def test_tags_create_category_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create(1, '')

@pytest.mark.vcr()
def test_tags_create_value_typerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', 1)

@pytest.mark.vcr()
def test_tags_create_description_typerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', '', description=1)

@pytest.mark.vcr()
def test_tags_create_category_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', '', category_description=1)

pytest.mark.vcr()
def test_tags_create_all_users_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', '', all_users_permissions=1)

@pytest.mark.vcr()
def test_tags_create_all_users_permissions_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.create('', '', all_users_permissions=['something'])

@pytest.mark.vcr()
def test_tags_create_current_domain_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', '', current_domain_permissions=1)

@pytest.mark.vcr()
def test_tags_create_filters_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', '', filters=1)

@pytest.mark.vcr()
def test_tags_create_success(api, tagvalue):
    assert isinstance(tagvalue, dict)
    check(tagvalue, 'uuid', 'uuid')
    check(tagvalue, 'created_at', 'datetime')
    check(tagvalue, 'updated_at', 'datetime')
    check(tagvalue, 'updated_by', str)
    check(tagvalue, 'category_uuid', 'uuid')
    check(tagvalue, 'value', str)
    # check(tagvalue, 'description', str, allow_none=True)
    # check(tagvalue, 'category_description', str, allow_none=True)
    check(tagvalue, 'access_control', dict)
    check(tagvalue['access_control'], 'all_users_permissions', list)
    check(tagvalue['access_control'], 'current_domain_permissions', list)
    check(tagvalue['access_control'], 'current_user_permissions', list)
    check(tagvalue['access_control'], 'defined_domain_permissions', list)
    # check(tagvalue, 'filters', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_create_filters_and_access_control_success(api, user, tagfilters):
    tagvalue = api.tags.create('Example', 'Test',
        all_users_permissions=['CAN_EDIT'],
        current_domain_permissions=[(user['uuid'], user['username'], 'user', ['CAN_EDIT'])],
        filters=tagfilters)
    assert isinstance(tagvalue, dict)
    check(tagvalue, 'uuid', 'uuid')
    check(tagvalue, 'created_at', 'datetime')
    check(tagvalue, 'updated_at', 'datetime')
    check(tagvalue, 'updated_by', str)
    check(tagvalue, 'category_uuid', 'uuid')
    check(tagvalue, 'value', str)
    # check(tagvalue, 'description', str, allow_none=True)
    # check(tagvalue, 'category_description', str, allow_none=True)
    check(tagvalue, 'access_control', dict)
    check(tagvalue['access_control'], 'all_users_permissions', list)
    check(tagvalue['access_control'], 'current_domain_permissions', list)
    check(tagvalue['access_control'], 'current_user_permissions', list)
    check(tagvalue['access_control'], 'defined_domain_permissions', list)
    check(tagvalue, 'filters', dict, allow_none=True)
    api.tags.delete(tagvalue['uuid'])

@pytest.mark.vcr()
def test_tags_create_category_name_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create_category(1)

@pytest.mark.vcr()
def test_tags_create_category_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create_category('', description=1)

@pytest.mark.vcr()
def test_tags_create_category_success(api, tagcat):
    assert isinstance(tagcat, dict)
    check(tagcat, 'uuid', 'uuid')
    check(tagcat, 'created_at', 'datetime')
    check(tagcat, 'updated_at', 'datetime')
    check(tagcat, 'updated_by', str)
    check(tagcat, 'name', str)
    #check(tagcat, 'description', str, allow_none=True)
    check(tagcat, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_delete_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.delete(1)

@pytest.mark.vcr()
def test_tags_delete_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.delete('1')

@pytest.mark.vcr()
def test_tags_delete_success(api, tagvalue):
    api.tags.delete(tagvalue['uuid'])

@pytest.mark.vcr()
def test_tags_delete_category_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.delete_category(1)

@pytest.mark.vcr()
def test_tags_delete_category_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.delete_category('1')

@pytest.mark.vcr()
def test_tags_delete_category_success(api, tagcat):
    api.tags.delete_category(tagcat['uuid'])

@pytest.mark.vcr()
def test_tags_details_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.details(1)

@pytest.mark.vcr()
def test_tags_details_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.details('1')

@pytest.mark.vcr()
def test_tags_details_success(api, tagvalue):
    t = api.tags.details(tagvalue['uuid'])
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'category_uuid', 'uuid')
    check(t, 'value', str)
    check(t, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_details_category_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.details_category(1)

@pytest.mark.vcr()
def test_tags_details_category_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.details_category('1')

@pytest.mark.vcr()
def test_tags_details_category_success(api, tagcat):
    t = api.tags.details_category(tagcat['uuid'])
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'name', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_edit_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit(1)

@pytest.mark.vcr()
def test_tags_edit_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.edit('1')

@pytest.mark.vcr()
def test_tags_edit_value_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), value=1)

@pytest.mark.vcr()
def test_tags_edit_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), description=1)

@pytest.mark.vcr()
def test_tags_edit_success(api, tagvalue):
    t = api.tags.edit(tagvalue['uuid'], value='Edited')
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'category_uuid', 'uuid')
    check(t, 'value', str)
    check(t, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)
    assert t['value'] == 'Edited'

@pytest.mark.vcr()
def test_tags_edit_category_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit_category(1)

@pytest.mark.vcr()
def test_tags_edit_category_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.edit_category('1')

@pytest.mark.vcr()
def test_tags_edit_category_value_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), value=1)

@pytest.mark.vcr()
def test_tags_edit_category_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), description=1)

@pytest.mark.vcr()
def test_tags_edit_category_success(api, tagcat):
    t = api.tags.edit_category(tagcat['uuid'], name='Edited')
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'name', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'reserved', bool)
    assert t['name'] == 'Edited'

def test_tags_list_constructor_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, True, None)

def test_tags_list_constructor_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, 'nadda', None)

def test_tags_list_constructor_filter_type_success(api):
    resp = api.tags._tag_list_constructor([],
        api.tags._filterset_tags, 'and', None)
    assert resp['ft'] == 'AND'

def test_tags_list_constructor_sort_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, None, 1)

def test_tags_list_constructor_sort_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, None, (('something_else'),))

def test_tags_list_constructor_sort_success(api):
    resp = api.tags._tag_list_constructor([],
        api.tags._filterset_tags, None, (('value','asc'),))
    assert resp['sort'] == 'value:asc'

def test_tags_list_constructor_filter_success(api):
    resp = api.tags._tag_list_constructor([
        ('value', 'eq', 'Test')
    ], api.tags._filterset_tags, None, None)
    assert resp['f'] == ['value:eq:Test']

@pytest.mark.vcr()
def test_tags_list_success(api, tagvalue):
    tags = api.tags.list()
    assert isinstance(tags, TagsIterator)
    t = tags.next()
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'category_uuid', 'uuid')
    check(t, 'value', str)
    check(t, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_list_category_success(api, tagcat):
    tags = api.tags.list_categories()
    assert isinstance(tags, TagsIterator)
    t = tags.next()
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'name', str)
    #check(t, 'description', str, allow_none=True)
    #check(t, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_list_date_failure(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.list(('updated_at', 'eq', 'something_else'))

@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.assign(1, [])

@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.assign([1,], [])

@pytest.mark.vcr()
def test_tags_assign_assets_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.assign(['something'], [])

@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.assign([], 1)

@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.assign([], [1, ])

@pytest.mark.vcr()
def test_tags_assign_tags_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.assign([], ['something', ])

@pytest.mark.vcr()
def test_tags_assign_success(api, tagvalue):
    assets = api.assets.list()
    resp = api.tags.assign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)

@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.unassign(1, [])

@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.unassign([1,], [])

@pytest.mark.vcr()
def test_tags_unassign_assets_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign(['something'], [])

@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.unassign([], 1)

@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.unassign([], [1, ])

@pytest.mark.vcr()
def test_tags_unassign_tags_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign([], ['something', ])

@pytest.mark.vcr()
def test_tags_unassign_success(api, tagvalue):
    assets = api.assets.list()
    resp = api.tags.unassign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)