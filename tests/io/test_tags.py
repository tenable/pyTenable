'''
test tags
'''
import uuid
import pytest
from tests.checker import check, single
from tenable.errors import UnexpectedValueError, NotFoundError
from tenable.io.tags import TagsIterator


@pytest.fixture(name='tagfilters')
def fixture_tagfilters():
    '''
    Returns tag filter structure
    '''
    return [('ipv4', 'eq', ['192.168.0.0/24'])]


@pytest.fixture(name='filterdefs')
def fixture_filterdefs():
    '''
    Returns filter definition of ipv4 type filter
    '''
    return {
        'ipv4': {
            'choices': None,
            'operators': ['eq'],
            'pattern':
                '^(\\s*((?=\\d+\\.\\d+\\.\\d+\\.\\d+(?:\\/|-|\\s*,|$))'
                '(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})'
                '(?:(?:\\/(?:3[0-2]|[12]+\\d|[1-9]))|((?:-(?=\\d+\\.\\d+\\.\\d+\\.\\d+)'
                '(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})|(?:\\s*,(?:\\s*)))?)+)+$'},
    }


@pytest.fixture(name='tagvalue')
@pytest.mark.vcr()
def fixture_tagvalue(request, api):
    '''
    Fixture to create tag value
    '''
    tag = api.tags.create('Example', 'Test Tag3')

    def teardown():
        '''
        cleanup function to delete tag value
        '''
        try:
            api.tags.delete(tag['uuid'])
        except NotFoundError:
            pass

    request.addfinalizer(teardown)
    return tag


@pytest.fixture(name='tagcat')
@pytest.mark.vcr()
def fixture_tagcat(request, api):
    '''
    Fixture to create tag category
    '''
    tag = api.tags.create_category('Example3')

    def teardown():
        '''
        cleanup function to delete tag category
        '''
        try:
            api.tags.delete_category(tag['uuid'])
        except NotFoundError:
            pass

    request.addfinalizer(teardown)
    return tag


def test_tags_permission_constructor_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([(1, 'something', 'user')])


def test_tags_permission_constructor_id_unexpectedvalueerror(api):
    '''
    test to raise exception when id param value does not match the pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_permission_constructor')([('something', 'something', 'user')])


def test_tags_permission_constructor_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([(str(uuid.uuid4()), 1, 'user')])


def test_tags_permission_constructor_type_typeerror(api):
    '''
    test to raise exception when type of type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([(str(uuid.uuid4()), 'something', 1)])


def test_tags_permission_constructor_type_unexpectedvalueerror(api):
    '''
    test to raise exception when type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_permission_constructor')([
            (str(uuid.uuid4()), 'something', 'something')])


def test_tags_permission_constructor_permissions_typeerror(api):
    '''
    test to raise exception when type of permissions param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([
            (str(uuid.uuid4()), 'something', 'user', 1)])


def test_tags_permission_constructor_permissions_unexpectedvalueerror(api):
    '''
    test to raise exception when permissions param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_permission_constructor')([
            (str(uuid.uuid4()), 'something', 'user', ['something'])])


def test_tags_permission_constructor_dict_id_typeerror(api):
    '''
    test to raise exception when type of id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([{
            'id': 1,
            "name": 'something',
            "type": 'something',
            "permissions": [],
        }])


def test_tags_permission_constructor_dict_id_unexpectedvalueerror(api):
    '''
    test to raise exception when id param value does not match the pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_permission_constructor')([{
            'id': 'something',
            "name": 'something',
            "type": 'something',
            "permissions": [],
        }])


def test_tags_permission_constructor_dict_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([{
            'id': str(uuid.uuid4()),
            "name": 1,
            "type": 'something',
            "permissions": [],
        }])


def test_tags_permission_constructor_dict_type_typeerror(api):
    '''
    test to raise exception when type of type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 1,
            "permissions": [],
        }])


def test_tags_permission_constructor_dict_type_unexpectedvalueerror(api):
    '''
    test to raise exception when type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_permission_constructor')([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 'something',
            "permissions": [],
        }])


def test_tags_permission_constructor_dict_permission_typeerror(api):
    '''
    test to raise exception when type of permission param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_permission_constructor')([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 'user',
            "permissions": 1,
        }])


def test_tags_permission_constructor_dict_permission_unexpectedvalueerror(api):
    '''
    test to raise exception when permission param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_permission_constructor')([{
            'id': str(uuid.uuid4()),
            "name": 'something',
            "type": 'user',
            "permissions": ['something'],
        }])


def test_tags_permission_constructor_tuple_pass(api):
    '''
    test to parse tuple type current_domain_permissions
    '''
    user = str(uuid.uuid4())
    assert getattr(api.tags, '_permission_constructor')([
        (user, 'test', 'user', ['CAN_EDIT'])
    ]) == [{'permissions': ['CAN_EDIT'], 'type': 'USER', 'name': 'test', 'id': user}]

    # when permissions not passed
    assert getattr(api.tags, '_permission_constructor')([
        (user, 'test', 'user')
    ]) == [{'permissions': [], 'type': 'USER', 'name': 'test', 'id': user}]


def test_tags_permission_constructor_dict_pass(api):
    '''
    test to parse dict type current_domain_permission
    '''
    user = str(uuid.uuid4())
    assert getattr(api.tags, '_permission_constructor')([
        {'id': user, 'name': 'test', 'type': 'user', 'permissions': ['CAN_EDIT']}
    ]) == [{'permissions': ['CAN_EDIT'], 'type': 'USER', 'name': 'test', 'id': user}]

    # when permissions not passed
    assert getattr(api.tags, '_permission_constructor')([
        {'id': user, 'name': 'test', 'type': 'user'}
    ]) == [{'permissions': [], 'type': 'USER', 'name': 'test', 'id': user}]


def test_tags_tag_value_constructor_filter_type_typeerror(api, tagfilters, filterdefs):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_tag_value_constructor')(
            filters=tagfilters, filterdefs=filterdefs, filter_type=1)


def test_tags_tag_value_constructor_filter_type_unexpectedvalueerror(api, tagfilters, filterdefs):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_tag_value_constructor')(filters=tagfilters,
                                                    filterdefs=filterdefs, filter_type='nope')


def test_tags_tag_value_constructor_pass(api, tagfilters, filterdefs):
    '''
    test to parse tag value filters
    '''
    assert getattr(api.tags, '_tag_value_constructor')(
        filters=tagfilters, filterdefs=filterdefs, filter_type='and'
    ) == {'asset': {'and': [{'field': 'ipv4', 'operator': 'eq', 'value': '192.168.0.0/24'}]}}


@pytest.mark.vcr()
def test_tags_create_category_typeerror(api):
    '''
    test to raise exception when type of category param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create(1, '')


@pytest.mark.vcr()
def test_tags_create_value_typerror(api):
    '''
    test to raise exception when type of value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', 1)


@pytest.mark.vcr()
def test_tags_create_value_description_typerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', '', description=1)


@pytest.mark.vcr()
def test_tags_create_value_category_description_typeerror(api):
    '''
    test to raise exception when type of category_description
    param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', '', category_description=1)


@pytest.mark.vcr()
def test_tags_create_all_users_permissions_typeerror(api):
    '''
    test to raise exception when type of all_users_permissions param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', '', all_users_permissions=1)


@pytest.mark.vcr()
def test_tags_create_all_users_permissions_unexpectedvalueerror(api):
    '''
    test to raise exception when all_users_permission param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.create('', '', all_users_permissions=['something'])


@pytest.mark.vcr()
def test_tags_create_current_domain_permissions_typeerror(api):
    '''
    test to raise exception when type of current_domain_permission param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', '', current_domain_permissions=1)


@pytest.mark.vcr()
def test_tags_create_filters_typeerror(api):
    '''
    test to raise exception when type of filters param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', '', filters=1)


@pytest.mark.vcr()
def test_tags_create_success(tagvalue):
    '''
    test to create tag value.
    '''
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
    '''
    test to create tag value and assign all_users_permissions,
    current_domain_permission and filters
    '''
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
    assert tagvalue['access_control']['all_users_permissions'] == ['CAN_EDIT']
    assert any(v['id'] == user['uuid']
               for v in tagvalue['access_control']['current_domain_permissions'])
    assert tagvalue['filters'] == {
        'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"192.168.0.0/24"}]}'}
    api.tags.delete(tagvalue['uuid'])


@pytest.mark.vcr()
def test_tags_create_category_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create_category(1)


@pytest.mark.vcr()
def test_tags_create_category_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create_category('', description=1)


@pytest.mark.vcr()
def test_tags_create_category_success(tagcat):
    '''
    test to create tag category.
    '''
    assert isinstance(tagcat, dict)
    check(tagcat, 'uuid', 'uuid')
    check(tagcat, 'created_at', 'datetime')
    check(tagcat, 'updated_at', 'datetime')
    check(tagcat, 'updated_by', str)
    check(tagcat, 'name', str)
    # check(tagcat, 'description', str, allow_none=True)
    check(tagcat, 'reserved', bool)


@pytest.mark.vcr()
def test_tags_delete_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.delete(1)


@pytest.mark.vcr()
def test_tags_delete_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.delete('1')


@pytest.mark.vcr()
def test_tags_delete_success(api, tagvalue):
    '''
    test to delete tag value.
    '''
    api.tags.delete(tagvalue['uuid'])


@pytest.mark.vcr()
def test_tags_delete_bulk_typeerror(api, tagvalue):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.delete(tagvalue['uuid'], 1)


@pytest.mark.vcr()
def test_tags_delete_bulk_unexpectedvalueerror(api, tagvalue):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.delete(tagvalue['uuid'], 'nope')


@pytest.mark.vcr()
def test_tags_delete_bulk_success(api):
    '''
    test to delete multiple tags .
    '''
    tag1 = api.tags.create('Example', 'Test1')
    tag2 = api.tags.create('Example', 'Test2')
    api.tags.delete(tag1['uuid'], tag2['uuid'])


@pytest.mark.vcr()
def test_tags_delete_category_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.delete_category(1)


@pytest.mark.vcr()
def test_tags_delete_category_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.delete_category('1')


@pytest.mark.vcr()
def test_tags_delete_category_success(api, tagcat):
    '''
    test to delete tag category.
    '''
    api.tags.delete_category(tagcat['uuid'])


@pytest.mark.vcr()
def test_tags_details_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.details(1)


@pytest.mark.vcr()
def test_tags_details_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.details('1')


@pytest.mark.vcr()
def test_tags_details_success(api, tagvalue):
    '''
    test to get details for a specific tag category/value pair.
    '''
    details = api.tags.details(tagvalue['uuid'])
    assert isinstance(details, dict)
    check(details, 'uuid', 'uuid')
    check(details, 'created_at', 'datetime')
    check(details, 'created_by', str)
    check(details, 'updated_at', 'datetime')
    check(details, 'updated_by', str)
    check(details, 'category_uuid', 'uuid')
    check(details, 'value', str)
    check(details, 'type', str)
    # check(t, 'description', str, allow_none=True)
    check(details, 'category_name', str)
    # check(t, 'category_description', str, allow_none=True)


@pytest.mark.vcr()
def test_tags_details_category_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.details_category(1)


@pytest.mark.vcr()
def test_tags_details_category_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.details_category('1')


@pytest.mark.vcr()
def test_tags_details_category_success(api, tagcat):
    '''
    test to get details for a specific tag category.
    '''
    details = api.tags.details_category(tagcat['uuid'])
    assert isinstance(details, dict)
    check(details, 'uuid', 'uuid')
    check(details, 'created_at', 'datetime')
    check(details, 'created_by', str)
    check(details, 'updated_at', 'datetime')
    check(details, 'updated_by', str)
    check(details, 'name', str)
    # check(t, 'description', str, allow_none=True)
    check(details, 'reserved', bool)


@pytest.mark.vcr()
def test_tags_edit_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(1)


@pytest.mark.vcr()
def test_tags_edit_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.edit('1')


@pytest.mark.vcr()
def test_tags_edit_value_typeerror(api):
    '''
    test to raise exception when type of value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), value=1)


@pytest.mark.vcr()
def test_tags_edit_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), description=1)


@pytest.mark.vcr()
def test_tags_edit_all_users_permissions_typeerror(api, tagvalue):
    '''
    test to raise exception when type of all_users_permission param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(tagvalue['uuid'], all_users_permissions=1)


@pytest.mark.vcr()
def test_tags_edit_all_users_permissions_unexpectedvalueerror(api, tagvalue):
    '''
    test to raise exception when all_users_permission param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.edit(tagvalue['uuid'], all_users_permissions=['something'])


@pytest.mark.vcr()
def test_tags_edit_current_domain_permissions_typeerror(api, tagvalue):
    '''
    test to raise exception when type of current_domain_permission param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(tagvalue['uuid'], current_domain_permissions=1)


@pytest.mark.vcr()
def test_tags_edit_filters_typeerror(api, tagvalue):
    '''
    test to raise exception when type of filters param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(tagvalue['uuid'], filters=1)


@pytest.mark.vcr()
def test_tags_edit_success(api, tagvalue):
    '''
    test to edit tag category/value pair information.
    '''
    resp = api.tags.edit(tagvalue['uuid'], value='Edited')
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'category_uuid', 'uuid')
    check(resp, 'value', str)
    check(resp, 'type', str)
    # check(t, 'description', str, allow_none=True)
    check(resp, 'category_name', str)
    # check(t, 'category_description', str, allow_none=True)
    check(resp, 'access_control', dict)
    check(resp['access_control'], 'all_users_permissions', list)
    check(resp['access_control'], 'current_domain_permissions', list)
    check(resp['access_control'], 'current_user_permissions', list)
    check(resp['access_control'], 'defined_domain_permissions', list)
    # check(tagvalue, 'filters', dict, allow_none=True)
    assert resp['value'] == 'Edited'


@pytest.mark.vcr()
def test_tags_edit_filters_and_access_control_success(api, user, tagfilters):
    '''
    test to edit tag value and update all_users_permissions,
    current_domain_permission and filters
    '''
    tagvalue = api.tags.create('Example', 'Test',
                               all_users_permissions=['CAN_EDIT'],
                               current_domain_permissions=[(user['uuid'], user['username'], 'user', ['CAN_EDIT'])],
                               filters=tagfilters)
    resp = api.tags.edit(tagvalue['uuid'], filters=[('ipv4', 'eq', ['127.0.0.1'])],
                         all_users_permissions=[], current_domain_permissions=[])
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'category_uuid', 'uuid')
    check(resp, 'value', str)
    check(resp, 'type', str)
    # check(t, 'description', str, allow_none=True)
    check(resp, 'category_name', str)
    # check(t, 'category_description', str, allow_none=True)
    check(resp, 'access_control', dict)
    check(resp['access_control'], 'all_users_permissions', list)
    check(resp['access_control'], 'current_domain_permissions', list)
    check(resp['access_control'], 'current_user_permissions', list)
    check(resp['access_control'], 'defined_domain_permissions', list)
    check(tagvalue, 'filters', dict, allow_none=True)
    assert resp['access_control']['all_users_permissions'] == []
    assert not any(v['id'] == user['uuid']
                   for v in resp['access_control']['current_domain_permissions'])
    assert resp['filters'] == {
        'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"127.0.0.1"}]}'}
    assert resp['access_control']['version'] == 1
    api.tags.delete(tagvalue['uuid'])


@pytest.mark.vcr()
def test_tags_edit_category_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit_category(1)


@pytest.mark.vcr()
def test_tags_edit_category_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.edit_category('1')


@pytest.mark.vcr()
def test_tags_edit_category_value_typeerror(api):
    '''
    test to raise exception when type of value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), value=1)


@pytest.mark.vcr()
def test_tags_edit_category_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), description=1)


@pytest.mark.vcr()
def test_tags_edit_category_success(api, tagcat):
    '''
    test to edit tag category information.
    '''
    resp = api.tags.edit_category(tagcat['uuid'], name='Edited')
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'name', str)
    # check(t, 'description', str, allow_none=True)
    check(resp, 'reserved', bool)
    assert resp['name'] == 'Edited'


def test_tags_list_constructor_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_tag_list_constructor')([],
                                                   getattr(api.tags, '_filterset_tags'), True, None)


def test_tags_list_constructor_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_tag_list_constructor')([],
                                                   getattr(api.tags, '_filterset_tags'), 'nadda', None)


def test_tags_list_constructor_filter_type_success(api):
    '''
    test to check filter_type param in tags_list_constructor method.
    '''
    resp = getattr(api.tags, '_tag_list_constructor')([],
                                                      getattr(api.tags, '_filterset_tags'), 'and', None)
    assert resp['ft'] == 'AND'


def test_tags_list_constructor_sort_typeerror(api):
    '''
    test to raise exception when type of sort param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.tags, '_tag_list_constructor')([],
                                                   getattr(api.tags, '_filterset_tags'), None, 1)


def test_tags_list_constructor_sort_unexpectedvalueerror(api):
    '''
    test to raise exception when sort param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.tags, '_tag_list_constructor')([],
                                                   getattr(api.tags, '_filterset_tags'), None, (('something_else'),))


def test_tags_list_constructor_sort_success(api):
    '''
    test to check sort param in tags_list_constructor method.
    '''
    resp = getattr(api.tags, '_tag_list_constructor')([],
                                                      getattr(api.tags, '_filterset_tags'), None, (('value', 'asc'),))
    assert resp['sort'] == 'value:asc'


def test_tags_list_constructor_filter_success(api):
    '''
    test to check filter param in tags_list_constructor method.
    '''
    resp = getattr(api.tags, '_tag_list_constructor')([
        ('value', 'eq', 'Test')
    ], getattr(api.tags, '_filterset_tags'), None, None)
    assert resp['f'] == ['value:eq:Test']


@pytest.mark.vcr()
def test_tags_list_success(api):
    '''
    test to get list of tags.
    '''
    tags = api.tags.list()
    assert isinstance(tags, TagsIterator)
    resp = tags.next()
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'category_uuid', 'uuid')
    check(resp, 'value', str)
    check(resp, 'type', str)
    # check(t, 'description', str, allow_none=True)
    check(resp, 'category_name', str)
    # check(t, 'category_description', str, allow_none=True)


@pytest.mark.vcr()
def test_tags_list_category_success(api):
    '''
    test to list of tag categories.
    '''
    tags = api.tags.list_categories()
    assert isinstance(tags, TagsIterator)
    resp = tags.next()
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'name', str)
    # check(t, 'description', str, allow_none=True)
    # check(t, 'reserved', bool)


@pytest.mark.vcr()
def test_tags_list_date_failure(api):
    '''
    test to raise exception when value of filter tuple does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.list(('updated_at', 'eq', 'something_else'))


@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_list(api):
    '''
    test to raise exception when type of asset param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign(1, [])


@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_entity(api):
    '''
    test to raise exception when type of asset param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign([1, ], [])


@pytest.mark.vcr()
def test_tags_assign_assets_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when asset param value does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.assign(['something'], [])


@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_list(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign([], 1)


@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_entity(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign([], [1, ])


@pytest.mark.vcr()
def test_tags_assign_tags_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when tags param value does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.assign([], ['something', ])


@pytest.mark.vcr()
def test_tags_assign_success(api, tagvalue):
    '''
    test to assign tags to assets.
    '''
    assets = api.assets.list()
    resp = api.tags.assign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)


@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_list(api):
    '''
    test to raise exception when type of asstes param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign(1, [])


@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_entity(api):
    '''
    test to raise exception when type of assets param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign([1, ], [])


@pytest.mark.vcr()
def test_tags_unassign_assets_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when assets param value does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign(['something'], [])


@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_list(api):
    '''
    test to unassign tags from assets.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign([], 1)


@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_entity(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign([], [1, ])


@pytest.mark.vcr()
def test_tags_unassign_tags_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign([], ['something', ])


@pytest.mark.vcr()
def test_tags_unassign_success(api, tagvalue):
    '''
    test to raise exception when tags param value does not match the expected.
    '''
    assets = api.assets.list()
    resp = api.tags.unassign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)


@pytest.mark.vcr()
def test_tags_edit_without_filters(api):
    '''
    test to apply filters that are available in current payload when filter parameter is not passed.
    '''

    tags = api.tags.list()
    flag = True
    while flag:
        try:
            resp = tags.next()
            tag_id = resp['uuid']
            tag_details = api.tags.details(tag_id)
            if 'filters' in tag_details:
                api.tags.edit(tag_id)
                flag = False
        except:
            flag = False
