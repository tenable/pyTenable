"""
test tags
"""

import uuid

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError
from tenable.io.tags import TagsIterator
from tests.checker import check, single
from tests.pytenable_log_handler import log_exception

TAGS_ASSETS_FILTERS = {
    'filters': [
        {
            'control': {
                'readable_regex': 'e.g. 123e4567e89b12d3a456426655440000',
                'type': 'entry',
                'regex': '.*',
            },
            'name': 'tenable_uuid',
            'readable_name': 'Tenable UUID',
            'operators': ['eq', 'neq'],
        },
        {
            'control': {
                'readable_regex': 'e.g. 192.168.0.1, 10.0.0.0/24, 201.15.99.100-201.15.99.199',
                'type': 'entry',
                'regex': '^(\\s*((?=\\d+\\.\\d+\\.\\d+\\.\\d+(?:\\/|-|\\s*,|$))(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})(?:(?:\\/(?:3[0-2]|[12]+\\d|[1-9]))|((?:-(?=\\d+\\.\\d+\\.\\d+\\.\\d+)(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})|(?:\\s*,(?:\\s*)))?)+)+$',
            },
            'name': 'ipv4',
            'readable_name': 'IPv4 Address',
            'operators': ['eq'],
        },
    ]
}

TAGS_VALUES = {
    'uuid': 'e04f4d91-1892-4207-a5c0-58b2a771d454',
    'created_at': '2021-07-06T09:33:30.663Z',
    'created_by': 'pytenable_test_user@tenable.com',
    'updated_at': '2021-07-06T09:33:30.663Z',
    'updated_by': 'pytenable_test_user@tenable.com',
    'category_uuid': 'e15d55f5-a18a-4738-93ba-0afc733e064a',
    'value': 'Test Tag',
    'type': 'static',
    'category_name': 'Example',
    'assignment_count': 0,
    'access_control': {
        'current_user_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
        'defined_domain_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
        'all_users_permissions': [],
        'current_domain_permissions': [
            {
                'id': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'name': 'pytenable_test_user@tenable.com',
                'type': 'USER',
                'permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
            }
        ],
        'version': 0,
    },
    'saved_search': False,
}


@pytest.fixture(name='tagfilters')
def fixture_tagfilters():
    """
    Returns tag filter structure
    """
    return [('ipv4', 'eq', ['192.168.0.0/24'])]


@pytest.fixture(name='filterdefs')
def fixture_filterdefs():
    """
    Returns filter definition of ipv4 type filter
    """
    return {
        'ipv4': {
            'choices': None,
            'operators': ['eq'],
            'pattern': '^(\\s*((?=\\d+\\.\\d+\\.\\d+\\.\\d+(?:\\/|-|\\s*,|$))'
            '(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})'
            '(?:(?:\\/(?:3[0-2]|[12]+\\d|[1-9]))|((?:-(?=\\d+\\.\\d+\\.\\d+\\.\\d+)'
            '(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})|(?:\\s*,(?:\\s*)))?)+)+$',
        },
    }


@pytest.fixture(name='tagvalue')
def fixture_tagvalue():
    """
    Fixture to create tag value. Please note that If the tag value already exist
    in the instance, it deletes that tag and create one
    """
    return {
        'uuid': 'e04f4d91-1892-4207-a5c0-58b2a771d454',
        'created_at': '2021-07-06T09:33:30.663Z',
        'created_by': 'pytenable_test_user@tenable.com',
        'updated_at': '2021-07-06T09:33:30.663Z',
        'updated_by': 'pytenable_test_user@tenable.com',
        'category_uuid': 'e15d55f5-a18a-4738-93ba-0afc733e064a',
        'value': 'Test Tag',
        'type': 'static',
        'category_name': 'Example',
        'assignment_count': 0,
        'access_control': {
            'current_user_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
            'defined_domain_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
            'all_users_permissions': [],
            'current_domain_permissions': [
                {
                    'id': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                    'name': 'pytenable_test_user@tenable.com',
                    'type': 'USER',
                    'permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                }
            ],
            'version': 0,
        },
        'saved_search': False,
    }


@pytest.fixture(name='tagcat')
def fixture_tagcat():
    """
    Fixture to create tag category
    """
    return {
        'uuid': 'e6b4cd75-c71e-49d7-8174-0d16a1f9ee8b',
        'created_at': '2019-01-28T17:07:25.417Z',
        'created_by': 'test_admin@pytenable.io',
        'updated_at': '2019-01-28T17:07:25.417Z',
        'updated_by': 'test_admin@pytenable.io',
        'name': 'Example3',
        'reserved': False,
    }


@pytest.fixture(name='custom_tagvalue')
def fixture_custom_tagvalue(user):
    """
    Fixture to create tag value. Please note that If the tag value already exist
    in the instance, it deletes that tag and create one
    """
    return {
        'uuid': '001a56ef-2039-47c7-9dba-6ae6bd9c17c4',
        'created_at': '2021-07-08T18:15:06.232Z',
        'created_by': 'pytenable_test_user@tenable.com',
        'updated_at': '2021-07-08T18:15:06.232Z',
        'updated_by': 'pytenable_test_user@tenable.com',
        'category_uuid': 'e15d55f5-a18a-4738-93ba-0afc733e064a',
        'value': 'Custom Test',
        'type': 'dynamic',
        'category_name': 'Example',
        'assignment_count': 0,
        'access_control': {
            'current_user_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
            'defined_domain_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
            'all_users_permissions': ['CAN_EDIT'],
            'current_domain_permissions': [
                {
                    'id': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                    'name': 'pytenable_test_user@tenable.com',
                    'type': 'USER',
                },
                {'id': user['uuid'], 'name': user['username'], 'type': 'USER'},
            ],
            'version': 0,
        },
        'saved_search': False,
        'filters': {
            'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"192.168.0.0/24"}]}'
        },
    }


def test_tags_permission_constructor_id_typeerror(tvm):
    """
    test to raise exception when type of id param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')([(1, 'something', 'user')])


def test_tags_permission_constructor_id_unexpectedvalueerror(tvm):
    """
    test to raise exception when id param value does not match the pattern.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_permission_constructor')(
            [('something', 'something', 'user')]
        )


def test_tags_permission_constructor_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')([(str(uuid.uuid4()), 1, 'user')])


def test_tags_permission_constructor_type_typeerror(tvm):
    """
    test to raise exception when type of type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')(
            [(str(uuid.uuid4()), 'something', 1)]
        )


def test_tags_permission_constructor_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when type param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_permission_constructor')(
            [(str(uuid.uuid4()), 'something', 'something')]
        )


def test_tags_permission_constructor_permissions_typeerror(tvm):
    """
    test to raise exception when type of permissions param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')(
            [(str(uuid.uuid4()), 'something', 'user', 1)]
        )


def test_tags_permission_constructor_permissions_unexpectedvalueerror(tvm):
    """
    test to raise exception when permissions param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_permission_constructor')(
            [(str(uuid.uuid4()), 'something', 'user', ['something'])]
        )


def test_tags_permission_constructor_dict_id_typeerror(tvm):
    """
    test to raise exception when type of id param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')(
            [
                {
                    'id': 1,
                    'name': 'something',
                    'type': 'something',
                    'permissions': [],
                }
            ]
        )


def test_tags_permission_constructor_dict_id_unexpectedvalueerror(tvm):
    """
    test to raise exception when id param value does not match the pattern.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_permission_constructor')(
            [
                {
                    'id': 'something',
                    'name': 'something',
                    'type': 'something',
                    'permissions': [],
                }
            ]
        )


def test_tags_permission_constructor_dict_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')(
            [
                {
                    'id': str(uuid.uuid4()),
                    'name': 1,
                    'type': 'something',
                    'permissions': [],
                }
            ]
        )


def test_tags_permission_constructor_dict_type_typeerror(tvm):
    """
    test to raise exception when type of type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')(
            [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'something',
                    'type': 1,
                    'permissions': [],
                }
            ]
        )


def test_tags_permission_constructor_dict_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when type param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_permission_constructor')(
            [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'something',
                    'type': 'something',
                    'permissions': [],
                }
            ]
        )


def test_tags_permission_constructor_dict_permission_typeerror(tvm):
    """
    test to raise exception when type of permission param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_permission_constructor')(
            [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'something',
                    'type': 'user',
                    'permissions': 1,
                }
            ]
        )


def test_tags_permission_constructor_dict_permission_unexpectedvalueerror(tvm):
    """
    test to raise exception when permission param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_permission_constructor')(
            [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'something',
                    'type': 'user',
                    'permissions': ['something'],
                }
            ]
        )


def test_tags_permission_constructor_tuple_pass(tvm):
    """
    test to parse tuple type current_domain_permissions
    """
    user = str(uuid.uuid4())
    assert getattr(tvm.tags, '_permission_constructor')(
        [(user, 'test', 'user', ['CAN_EDIT'])]
    ) == [{'permissions': ['CAN_EDIT'], 'type': 'USER', 'name': 'test', 'id': user}]

    # when permissions not passed
    assert getattr(tvm.tags, '_permission_constructor')([(user, 'test', 'user')]) == [
        {'permissions': [], 'type': 'USER', 'name': 'test', 'id': user}
    ]


def test_tags_permission_constructor_dict_pass(tvm):
    """
    test to parse dict type current_domain_permission
    """
    user = str(uuid.uuid4())
    assert getattr(tvm.tags, '_permission_constructor')(
        [{'id': user, 'name': 'test', 'type': 'user', 'permissions': ['CAN_EDIT']}]
    ) == [{'permissions': ['CAN_EDIT'], 'type': 'USER', 'name': 'test', 'id': user}]

    # when permissions not passed
    assert getattr(tvm.tags, '_permission_constructor')(
        [{'id': user, 'name': 'test', 'type': 'user'}]
    ) == [{'permissions': [], 'type': 'USER', 'name': 'test', 'id': user}]


def test_tags_tag_value_constructor_filter_type_typeerror(tvm, tagfilters, filterdefs):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_tag_value_constructor')(
            filters=tagfilters, filterdefs=filterdefs, filter_type=1
        )


def test_tags_tag_value_constructor_filter_type_unexpectedvalueerror(
    tvm, tagfilters, filterdefs
):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_tag_value_constructor')(
            filters=tagfilters, filterdefs=filterdefs, filter_type='nope'
        )


def test_tags_tag_value_constructor_pass(tvm, tagfilters, filterdefs):
    """
    test to parse tag value filters
    """
    assert getattr(tvm.tags, '_tag_value_constructor')(
        filters=tagfilters, filterdefs=filterdefs, filter_type='and'
    ) == {
        'asset': {
            'and': [{'field': 'ipv4', 'operator': 'eq', 'value': '192.168.0.0/24'}]
        }
    }


def test_tags_create_category_typeerror(tvm):
    """
    test to raise exception when type of category param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.create(1, '')


def test_tags_create_value_typerror(tvm):
    """
    test to raise exception when type of value param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.create('', 1)


def test_tags_create_value_description_typerror(tvm):
    """
    test to raise exception when type of description param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.create('', '', description=1)


def test_tags_create_value_category_description_typeerror(tvm):
    """
    test to raise exception when type of category_description
    param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.create(
            'a7b7ebf6-8aaf-4509-a5b3-872b7647fa86', '', category_description=1
        )


def test_tags_create_all_users_permissions_typeerror(tvm):
    """
    test to raise exception when type of all_users_permissions param
    does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.create('', '', all_users_permissions=1)


def test_tags_create_all_users_permissions_unexpectedvalueerror(tvm):
    """
    test to raise exception when all_users_permission param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.create('', '', all_users_permissions=['something'])


def test_tags_create_current_domain_permissions_typeerror(tvm):
    """
    test to raise exception when type of current_domain_permission param
    does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.create('', '', current_domain_permissions=1)


def test_tags_create_filters_typeerror(tvm):
    """
    test to raise exception when type of filters param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.create('', '', filters=1)


@responses.activate
def test_tags_create_success(tvm, tagvalue):
    """
    test to create tag value.
    """
    responses.add(responses.POST, 'https://nourl/tags/values', json=tagvalue)
    tagvalue = tvm.tags.create('Example', tagvalue['value'])
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


@responses.activate
def test_tags_create_filters_and_access_control_success(
    tvm, tagfilters, user, custom_tagvalue
):
    """
    test to create tag value and assign all_users_permissions,
    current_domain_permission and filters
    """
    responses.add(
        responses.GET, 'https://nourl/tags/assets/filters', json=TAGS_ASSETS_FILTERS
    )
    responses.add(responses.POST, 'https://nourl/tags/values', json=custom_tagvalue)
    custom_tagvalue = tvm.tags.create(
        'Example',
        value=custom_tagvalue['value'],
        all_users_permissions=['CAN_EDIT'],
        current_domain_permissions=[
            (user['uuid'], user['username'], 'user', ['CAN_EDIT'])
        ],
        filters=tagfilters,
    )
    assert isinstance(custom_tagvalue, dict)
    check(custom_tagvalue, 'uuid', 'uuid')
    check(custom_tagvalue, 'created_at', 'datetime')
    check(custom_tagvalue, 'updated_at', 'datetime')
    check(custom_tagvalue, 'updated_by', str)
    check(custom_tagvalue, 'category_uuid', 'uuid')
    check(custom_tagvalue, 'value', str)
    # check(tagvalue, 'description', str, allow_none=True)
    # check(tagvalue, 'category_description', str, allow_none=True)
    check(custom_tagvalue, 'access_control', dict)
    check(custom_tagvalue['access_control'], 'all_users_permissions', list)
    check(custom_tagvalue['access_control'], 'current_domain_permissions', list)
    check(custom_tagvalue['access_control'], 'current_user_permissions', list)
    check(custom_tagvalue['access_control'], 'defined_domain_permissions', list)
    check(custom_tagvalue, 'filters', dict, allow_none=True)
    assert custom_tagvalue['access_control']['all_users_permissions'] == ['CAN_EDIT']
    assert any(
        v['id'] == user['uuid']
        for v in custom_tagvalue['access_control']['current_domain_permissions']
    )
    assert custom_tagvalue['filters'] == {
        'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"192.168.0.0/24"}]}'
    }


def test_tags_create_category_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    try:
        with pytest.raises(TypeError):
            tvm.tags.create_category(1)
    except Exception as err:
        log_exception(err)


def test_tags_create_category_description_typeerror(tvm):
    """
    test to raise exception when type of description param does not match the expected type.
    """
    try:
        with pytest.raises(TypeError):
            tvm.tags.create_category('', description=1)
    except Exception as err:
        log_exception(err)


@responses.activate
def test_tags_create_category_success(tvm, tagcat):
    """
    test to create tag category.
    """
    responses.add(responses.POST, 'https://nourl/tags/categories', json=tagcat)
    tagcat = tvm.tags.create_category(tagcat['name'])
    assert isinstance(tagcat, dict)
    check(tagcat, 'uuid', 'uuid')
    check(tagcat, 'created_at', 'datetime')
    check(tagcat, 'updated_at', 'datetime')
    check(tagcat, 'updated_by', str)
    check(tagcat, 'name', str)
    # check(tagcat, 'description', str, allow_none=True)
    check(tagcat, 'reserved', bool)


def test_tags_delete_uuid_typeerror(tvm):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.delete(1)


def test_tags_delete_uuid_unexpectedvalueerror(tvm):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.delete('1')


@responses.activate
def test_tags_delete_success(tvm, tagvalue):
    """
    test to delete tag value.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
    )
    tvm.tags.delete(tagvalue['uuid'])


def test_tags_delete_bulk_typeerror(tvm, tagvalue):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.delete(tagvalue['uuid'], 1)


def test_tags_delete_bulk_unexpectedvalueerror(tvm, tagvalue):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.delete(tagvalue['uuid'], 'nope')


@responses.activate
def test_tags_delete_bulk_success(tvm):
    """
    test to delete multiple tags .
    """
    responses.add(
        responses.POST,
        'https://nourl/tags/values',
        json={
            'uuid': 'f3064567-173d-4326-ae81-8edd058e717b',
            'created_at': '2021-04-08T13:30:16.836Z',
            'created_by': 'tbalwani.ctr+pyt@tenable.com',
            'updated_at': '2021-04-08T13:30:16.836Z',
            'updated_by': 'tbalwani.ctr+pyt@tenable.com',
            'category_uuid': '45d8a9bf-913e-4779-bca0-25932c8afb54',
            'value': 'Test1',
            'type': 'static',
            'category_name': 'Example',
            'assignment_count': 0,
            'access_control': {
                'current_user_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                'defined_domain_permissions': [
                    'ALL',
                    'CAN_EDIT',
                    'CAN_SET_PERMISSIONS',
                ],
                'all_users_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                'current_domain_permissions': [],
            },
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/tags/values',
        json={
            'uuid': '3826fbbd-bd29-451c-9469-4be913d42811',
            'created_at': '2021-04-08T13:30:18.048Z',
            'created_by': 'tbalwani.ctr+pyt@tenable.com',
            'updated_at': '2021-04-08T13:30:18.048Z',
            'updated_by': 'tbalwani.ctr+pyt@tenable.com',
            'category_uuid': '45d8a9bf-913e-4779-bca0-25932c8afb54',
            'value': 'Test2',
            'type': 'static',
            'category_name': 'Example',
            'assignment_count': 0,
            'access_control': {
                'current_user_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                'defined_domain_permissions': [
                    'ALL',
                    'CAN_EDIT',
                    'CAN_SET_PERMISSIONS',
                ],
                'all_users_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                'current_domain_permissions': [],
            },
        },
    )
    responses.add(responses.POST, 'https://nourl/tags/values/delete-requests')
    tag1 = tvm.tags.create('Example', str(uuid.uuid4()))
    tag2 = tvm.tags.create('Example', str(uuid.uuid4()))
    tvm.tags.delete(tag1['uuid'], tag2['uuid'])


def test_tags_delete_category_uuid_typeerror(tvm):
    """
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.delete_category(1)


def test_tags_delete_category_uuid_unexpectedvalueerror(tvm):
    """
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.delete_category('1')


@responses.activate
def test_tags_delete_category_success(tvm, tagcat):
    """
    test to delete tag category.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/tags/categories/e6b4cd75-c71e-49d7-8174-0d16a1f9ee8b',
    )
    tvm.tags.delete_category(tagcat['uuid'])


def test_tags_details_uuid_typeerror(tvm):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.details(1)


def test_tags_details_unexpectedvalueerror(tvm):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.details('1')


@responses.activate
def test_tags_details_success(tvm, tagvalue):
    """
    test to get details for a specific tag category/value pair.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
        json=TAGS_VALUES,
    )
    details = tvm.tags.details(tagvalue['uuid'])
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


def test_tags_details_category_uuid_typeerror(tvm):
    """
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.details_category(1)


def test_tags_details_category_unexpectedvalueerror(tvm):
    """
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.details_category('1')


@responses.activate
def test_tags_details_category_success(tvm, tagcat):
    """
    test to get details for a specific tag category.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/categories/e6b4cd75-c71e-49d7-8174-0d16a1f9ee8b',
        json={
            'uuid': 'e6b4cd75-c71e-49d7-8174-0d16a1f9ee8b',
            'created_at': '2019-01-28T17:07:25.417Z',
            'created_by': 'test_admin@pytenable.io',
            'updated_at': '2019-01-28T17:07:25.417Z',
            'updated_by': 'test_admin@pytenable.io',
            'name': 'Example3',
            'reserved': False,
        },
    )
    details = tvm.tags.details_category(tagcat['uuid'])
    assert isinstance(details, dict)
    check(details, 'uuid', 'uuid')
    check(details, 'created_at', 'datetime')
    check(details, 'created_by', str)
    check(details, 'updated_at', 'datetime')
    check(details, 'updated_by', str)
    check(details, 'name', str)
    # check(t, 'description', str, allow_none=True)
    check(details, 'reserved', bool)


def test_tags_edit_uuid_typeerror(tvm):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.edit(1)


def test_tags_edit_uuid_unexpectedvalueerror(tvm):
    """
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.edit('1')


def test_tags_edit_value_typeerror(tvm):
    """
    test to raise exception when type of value param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.edit(uuid.uuid4(), value=1)


def test_tags_edit_description_typeerror(tvm):
    """
    test to raise exception when type of description param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.edit(uuid.uuid4(), description=1)


@responses.activate
def test_tags_edit_all_users_permissions_typeerror(tvm, tagvalue):
    """
    test to raise exception when type of all_users_permission param
    does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
        json=TAGS_VALUES,
    )
    with pytest.raises(TypeError):
        tvm.tags.edit(tagvalue['uuid'], all_users_permissions=1)


@responses.activate
def test_tags_edit_all_users_permissions_unexpectedvalueerror(tvm, tagvalue):
    """
    test to raise exception when all_users_permission param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
        json=TAGS_VALUES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.tags.edit(tagvalue['uuid'], all_users_permissions=['something'])


@responses.activate
def test_tags_edit_current_domain_permissions_typeerror(tvm, tagvalue):
    """
    test to raise exception when type of current_domain_permission param
    does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
        json=TAGS_VALUES,
    )
    with pytest.raises(TypeError):
        tvm.tags.edit(tagvalue['uuid'], current_domain_permissions=1)


@responses.activate
def test_tags_edit_filters_typeerror(tvm, tagvalue):
    """
    test to raise exception when type of filters param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
        json=TAGS_VALUES,
    )
    with pytest.raises(TypeError):
        tvm.tags.edit(tagvalue['uuid'], filters=1)


@responses.activate
def test_tags_edit_success(tvm, tagvalue):
    """
    test to edit tag category/value pair information.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
        json=TAGS_VALUES,
    )
    responses.add(
        responses.PUT,
        'https://nourl/tags/values/e04f4d91-1892-4207-a5c0-58b2a771d454',
        json={
            'uuid': 'e04f4d91-1892-4207-a5c0-58b2a771d454',
            'created_at': '2021-07-06T09:33:30.663Z',
            'created_by': 'pytenable_test_user@tenable.com',
            'updated_at': '2021-07-06T09:43:51.552Z',
            'updated_by': 'pytenable_test_user@tenable.com',
            'category_uuid': 'e15d55f5-a18a-4738-93ba-0afc733e064a',
            'value': 'Edited',
            'type': 'static',
            'category_name': 'Example',
            'assignment_count': 0,
            'access_control': {
                'current_user_permissions': [
                    'ALL',
                    'CAN_EDIT',
                    'CAN_SET_PERMISSIONS',
                ],
                'defined_domain_permissions': [
                    'ALL',
                    'CAN_EDIT',
                    'CAN_SET_PERMISSIONS',
                ],
                'all_users_permissions': [],
                'current_domain_permissions': [],
                'version': 0,
            },
            'saved_search': False,
        },
    )
    resp = tvm.tags.edit(tagvalue['uuid'], value='Edited')
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


@responses.activate
def test_tags_edit_filters_and_access_control_success(
    tvm, user, tagfilters, custom_tagvalue
):
    """
    test to edit tag value and update all_users_permissions,
    current_domain_permission and filters
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/assets/filters',
        json=TAGS_ASSETS_FILTERS,
    )
    responses.add(
        responses.GET,
        'https://nourl/tags/values/001a56ef-2039-47c7-9dba-6ae6bd9c17c4',
        json={
            'uuid': '001a56ef-2039-47c7-9dba-6ae6bd9c17c4',
            'created_at': '2021-07-08T18:15:06.232Z',
            'created_by': 'pytenable_test_user@tenable.com',
            'updated_at': '2021-07-08T18:15:06.232Z',
            'updated_by': 'pytenable_test_user@tenable.com',
            'category_uuid': 'e15d55f5-a18a-4738-93ba-0afc733e064a',
            'value': 'Custom Test',
            'type': 'dynamic',
            'category_name': 'Example',
            'assignment_count': 0,
            'access_control': {'version': 0},
            'saved_search': False,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/tags/values/001a56ef-2039-47c7-9dba-6ae6bd9c17c4',
        json={
            'uuid': '001a56ef-2039-47c7-9dba-6ae6bd9c17c4',
            'created_at': '2021-07-08T18:15:06.232Z',
            'created_by': 'pytenable_test_user@tenable.com',
            'updated_at': '2021-07-08T18:16:20.150Z',
            'updated_by': 'pytenable_test_user@tenable.com',
            'category_uuid': 'e15d55f5-a18a-4738-93ba-0afc733e064a',
            'value': 'Custom Test',
            'type': 'dynamic',
            'category_name': 'Example',
            'assignment_count': 0,
            'access_control': {
                'current_user_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                'defined_domain_permissions': [
                    'ALL',
                    'CAN_EDIT',
                    'CAN_SET_PERMISSIONS',
                ],
                'all_users_permissions': [],
                'current_domain_permissions': [
                    {
                        'id': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                        'name': 'pytenable_test_user@tenable.com',
                        'type': 'USER',
                        'permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                    }
                ],
                'version': 1,
            },
            'saved_search': False,
            'filters': {
                'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"127.0.0.1"}]}'
            },
        },
    )
    resp = tvm.tags.edit(
        custom_tagvalue['uuid'],
        filters=[('ipv4', 'eq', ['127.0.0.1'])],
        all_users_permissions=[],
        current_domain_permissions=[],
    )
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
    check(custom_tagvalue, 'filters', dict, allow_none=True)
    assert resp['access_control']['all_users_permissions'] == []
    assert not any(
        v['id'] == user['uuid']
        for v in resp['access_control']['current_domain_permissions']
    )
    assert resp['filters'] == {
        'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"127.0.0.1"}]}'
    }
    assert resp['access_control']['version'] == 1


def test_tags_edit_category_value_typeerror(tvm):
    """
    test to raise exception when type of value param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.edit_category(uuid.uuid4(), value=1)


def test_tags_edit_category_description_typeerror(tvm):
    """
    test to raise exception when type of description param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.edit_category(uuid.uuid4(), description=1)


@responses.activate
def test_tags_edit_category_success(tvm, tagcat):
    """
    test to edit tag category information.
    """
    responses.add(
        responses.PUT,
        'https://nourl/tags/categories/e6b4cd75-c71e-49d7-8174-0d16a1f9ee8b',
        json={
            'uuid': 'e6b4cd75-c71e-49d7-8174-0d16a1f9ee8b',
            'created_at': '2019-01-28T17:07:25.417Z',
            'created_by': 'test_admin@pytenable.io',
            'updated_at': '2019-01-28T17:33:01.021Z',
            'updated_by': 'test_admin@pytenable.io',
            'name': 'Edited',
            'reserved': False,
        },
    )
    resp = tvm.tags.edit_category(tagcat['uuid'], name='Edited')
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'name', str)
    check(resp, 'reserved', bool)
    assert resp['name'] == 'Edited'


def test_tags_list_constructor_filter_type_typeerror(tvm):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_tag_list_constructor')(
            [], getattr(tvm.tags, '_filterset_tags'), True, None
        )


def test_tags_list_constructor_filter_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_tag_list_constructor')(
            [], getattr(tvm.tags, '_filterset_tags'), 'nadda', None
        )


def test_tags_list_constructor_filter_type_success(tvm):
    """
    test to check filter_type param in tags_list_constructor method.
    """
    resp = getattr(tvm.tags, '_tag_list_constructor')(
        [], getattr(tvm.tags, '_filterset_tags'), 'and', None
    )
    assert resp['ft'] == 'AND'


def test_tags_list_constructor_sort_typeerror(tvm):
    """
    test to raise exception when type of sort param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.tags, '_tag_list_constructor')(
            [], getattr(tvm.tags, '_filterset_tags'), None, 1
        )


def test_tags_list_constructor_sort_unexpectedvalueerror(tvm):
    """
    test to raise exception when sort param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.tags, '_tag_list_constructor')(
            [], getattr(tvm.tags, '_filterset_tags'), None, (('something_else'),)
        )


def test_tags_list_constructor_sort_success(tvm):
    """
    test to check sort param in tags_list_constructor method.
    """
    resp = getattr(tvm.tags, '_tag_list_constructor')(
        [], getattr(tvm.tags, '_filterset_tags'), None, (('value', 'asc'),)
    )
    assert resp['sort'] == 'value:asc'


def test_tags_list_constructor_filter_success(tvm):
    """
    test to check filter param in tags_list_constructor method.
    """
    resp = getattr(tvm.tags, '_tag_list_constructor')(
        [('value', 'eq', 'Test')], getattr(tvm.tags, '_filterset_tags'), None, None
    )
    assert resp['f'] == ['value:eq:Test']


@responses.activate
def test_tags_list_success(tvm):
    """
    test to get list of tags.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values',
        json={
            'values': [
                {
                    'uuid': '8a3043ef-7f97-4a99-ba18-9a9004d14358',
                    'created_at': '2019-01-28T18:10:18.622Z',
                    'created_by': 'test_admin@pytenable.io',
                    'updated_at': '2019-01-28T18:10:18.622Z',
                    'updated_by': 'test_admin@pytenable.io',
                    'category_uuid': '1eb2e435-f321-49e7-bdf0-bcf9c3e47010',
                    'value': 'Test',
                    'type': 'static',
                    'category_name': 'Example',
                }
            ],
            'pagination': {'offset': 0, 'limit': 1000, 'total': 2},
        },
        match=[matchers.query_param_matcher({'limit': '1000', 'offset': '0'})],
    )
    tags = tvm.tags.list()
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


@responses.activate
def test_tags_list_category_success(tvm):
    """
    test to list of tag categories.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/categories',
        json={
            'categories': [
                {
                    'uuid': '09927518-3eb0-4f6a-bb95-1fff78708bb3',
                    'created_at': '2020-02-19T18:02:55.644Z',
                    'created_by': 'test_admin@pytenable.io',
                    'updated_at': '2020-02-19T18:02:55.644Z',
                    'updated_by': 'test_admin@pytenable.io',
                    'name': 'Example3',
                    'reserved': False,
                }
            ],
            'pagination': {'offset': 0, 'limit': 1000, 'total': 3},
        },
        match=[matchers.query_param_matcher({'limit': '1000', 'offset': '0'})],
    )
    tags = tvm.tags.list_categories()
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


def test_tags_list_date_failure(tvm):
    """
    test to raise exception when value of filter tuple does not match the expected.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.list(('updated_at', 'eq', 'something_else'))


def test_tags_assign_assets_typeerror_list(tvm):
    """
    test to raise exception when type of asset param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.assign(1, [])


def test_tags_assign_assets_typeerror_entity(tvm):
    """
    test to raise exception when type of asset param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.assign(
            [
                1,
            ],
            [],
        )


def test_tags_assign_assets_unexpectedvalueerror_entity(tvm):
    """
    test to raise exception when asset param value does not match the expected.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.assign(['something'], [])


def test_tags_assign_tags_typeerror_list(tvm):
    """
    test to raise exception when type of tags param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.assign([], 1)


def test_tags_assign_tags_typeerror_entity(tvm):
    """
    test to raise exception when type of tags param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.assign(
            [],
            [
                1,
            ],
        )


def test_tags_assign_tags_unexpectedvalueerror_entity(tvm):
    """
    test to raise exception when tags param value does not match the expected.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.assign(
            [],
            [
                'something',
            ],
        )


@responses.activate
def test_tags_assign_success(tvm, tagvalue):
    """
    test to assign tags to assets.
    """
    responses.add(
        responses.GET,
        'https://nourl/assets',
        json={'assets': [], 'total': 13},
    )
    responses.add(
        responses.POST,
        'https://nourl/tags/assets/assignments',
        json={'job_uuid': 'a308a251bd6afd2e899fbf0e204f29fa:5ae7a00e001687de8c12'},
    )
    assets = tvm.assets.list()
    resp = tvm.tags.assign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)


def test_tags_unassign_assets_typeerror_list(tvm):
    """
    test to raise exception when type of asstes param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.unassign(1, [])


def test_tags_unassign_assets_typeerror_entity(tvm):
    """
    test to raise exception when type of assets param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.unassign(
            [
                1,
            ],
            [],
        )


def test_tags_unassign_assets_unexpectedvalueerror_entity(tvm):
    """
    test to raise exception when assets param value does not match the expected.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.unassign(['something'], [])


def test_tags_unassign_tags_typeerror_list(tvm):
    """
    test to unassign tags from assets.
    """
    with pytest.raises(TypeError):
        tvm.tags.unassign([], 1)


def test_tags_unassign_tags_typeerror_entity(tvm):
    """
    test to raise exception when type of tags param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.tags.unassign(
            [],
            [
                1,
            ],
        )


def test_tags_unassign_tags_unexpectedvalueerror_entity(tvm):
    """
    test to raise exception when type of tags param does not match the expected type.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.tags.unassign(
            [],
            [
                'something',
            ],
        )


@responses.activate
def test_tags_unassign_success(tvm, tagvalue):
    """
    test to raise exception when tags param value does not match the expected.
    """
    responses.add(
        responses.GET,
        'https://nourl/assets',
        json={'assets': [], 'total': 13},
    )
    responses.add(
        responses.POST,
        'https://nourl/tags/assets/assignments',
        json={'job_uuid': '5588d733c5a2ba4ef94e8b88356fd571:6ebf32ac37193c964c24'},
    )
    assets = tvm.assets.list()
    resp = tvm.tags.unassign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)


@responses.activate
def test_tags_edit_without_filters(tvm):
    """
    test to apply filters that are available in current payload when filter parameter is not passed.
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/values',
        json={
            'values': [
                {
                    'uuid': '8fb1686f-7606-4594-821f-45defd53c302',
                    'created_at': '2021-05-11T09:01:37.579Z',
                    'created_by': 'pytenable_test_user@tenable.com',
                    'updated_at': '2021-06-22T14:16:39.216Z',
                    'updated_by': 'pytenable_test_user@tenable.com',
                    'category_uuid': 'f6d25769-f2d3-4dff-8283-1123e0351648',
                    'value': 'Test',
                    'description': '',
                    'type': 'dynamic',
                    'category_name': 'Test',
                    'category_description': '',
                }
            ],
            'pagination': {'offset': 0, 'limit': 1000, 'total': 2},
        },
        match=[matchers.query_param_matcher({'limit': '1000', 'offset': '0'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/tags/values/8fb1686f-7606-4594-821f-45defd53c302',
        json={
            'uuid': '8fb1686f-7606-4594-821f-45defd53c302',
            'created_at': '2021-05-11T09:01:37.579Z',
            'created_by': 'pytenable_test_user@tenable.com',
            'updated_at': '2021-06-22T14:16:39.216Z',
            'updated_by': 'pytenable_test_user@tenable.com',
            'category_uuid': 'f6d25769-f2d3-4dff-8283-1123e0351648',
            'value': 'Test',
            'description': '',
            'type': 'dynamic',
            'category_name': 'Test',
            'category_description': '',
            'assignment_count': 0,
            'access_control': {'version': 1},
            'filters': {
                'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"127.0.0.1"}]}'
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/tags/values/8fb1686f-7606-4594-821f-45defd53c302',
        json={
            'uuid': '8fb1686f-7606-4594-821f-45defd53c302',
            'created_at': '2021-05-11T09:01:37.579Z',
            'created_by': 'pytenable_test_user@tenable.com',
            'updated_at': '2021-06-22T14:43:01.906Z',
            'updated_by': 'pytenable_test_user@tenable.com',
            'category_uuid': 'f6d25769-f2d3-4dff-8283-1123e0351648',
            'value': 'Test',
            'description': '',
            'type': 'dynamic',
            'category_name': 'Test',
            'category_description': '',
            'assignment_count': 0,
            'access_control': {
                'current_user_permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                'defined_domain_permissions': [
                    'ALL',
                    'CAN_EDIT',
                    'CAN_SET_PERMISSIONS',
                ],
                'all_users_permissions': ['CAN_EDIT'],
                'current_domain_permissions': [
                    {
                        'id': 'eeea63a5-323b-4324-8c02-3aa260870641',
                        'name': 'dlx-test-user@tenable.com',
                        'type': 'USER',
                        'permissions': ['CAN_EDIT'],
                    },
                    {
                        'id': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                        'name': 'pytenable_test_user@tenable.com',
                        'type': 'USER',
                        'permissions': ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
                    },
                ],
                'version': 1,
            },
            'filters': {
                'asset': '{"and":[{"field":"ipv4","operator":"eq","value":"127.0.0.1"}]}'
            },
        },
    )

    tags = tvm.tags.list()
    flag = True
    while flag:
        try:
            resp = tags.next()
            tag_id = resp['uuid']
            tag_details = tvm.tags.details(tag_id)
            if 'filters' in tag_details:
                tvm.tags.edit(tag_id)
                flag = False
        except Exception as err:
            flag = False
            log_exception(err)


def tag_exists(tvm, tag_uuid):
    """function to check whether the tag value exists or not"""
    if tag_uuid in tvm.tags.list():
        return True
    else:
        return False


@responses.activate
def test_get_tag_uuid(tvm):
    """
    Test to fetch uuid from tag category and value
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/categories/filter-categories',
        json={
            'categories': [
                {
                    'uuid': '2225679d-cbde-4e44-a201-dadbd94fd700',
                    'name': 'test tag',
                    'value_count': 1,
                    'values': [
                        {'uuid': 'de2e56a2-6a0e-4757-8d00-e9ad635f6231', 'value': 'acr'}
                    ],
                }
            ]
        },
    )
    tag_uuid = tvm.tags.get_tag_uuid('test tag', 'acr')
    assert tag_uuid == 'de2e56a2-6a0e-4757-8d00-e9ad635f6231'
