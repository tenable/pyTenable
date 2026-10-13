"""
test credentials
"""

import io
import uuid

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError

from ..checker import check, single

CREDENTIALS = {
    'name': 'Example Cred',
    'description': '',
    'category': {'id': 'Host', 'name': 'Host'},
    'type': {'id': 'SSH', 'name': 'SSH'},
    'ad_hoc': False,
    'user_permissions': 64,
    'settings': {
        'username': 'root',
        'auth_method': 'password',
        'custom_password_prompt': '',
        'elevate_privileges_with': 'Nothing',
        'password': '********',
    },
    'permissions': [
        {
            'grantee_uuid': 'a09161a2-3860-4ca8-93c8-b3f7be366e50',
            'type': 'user',
            'permissions': 64,
            'name': 'test_admin@pytenable.io',
        }
    ],
}


def test_credentials_permissions_constructor_tuple_permission_type_typeerror(tvm):
    """test to raise the exception when type of permission type is not passed as defined"""

    with pytest.raises(TypeError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [(1, 32, str(uuid.uuid4()))]
        )


def test_credentials_permissions_constructor_tuple_permission_type_unexpectedvalueerror(
    tvm,
):
    """test to raise the exception when value of permission type is not passed as defined"""

    with pytest.raises(UnexpectedValueError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [('nope', 32, str(uuid.uuid4()))]
        )


def test_credentials_permissions_constructor_tuple_permission_permission_unexpectedvalueerror(
    tvm,
):
    """test to raise the exception when value of permission is not passed as defined"""
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [('user', 256, str(uuid.uuid4()))]
        )


def test_credentials_permissions_constructor_tuple_permission_uuid_typeerror(tvm):
    """test to raise the exception when type of permission is not passed as defined"""

    with pytest.raises(TypeError):
        getattr(tvm.credentials, '_permissions_constructor')([('user', 32, 1)])


def test_credentials_permissions_constructor_tuple_permission_uuid_unexpectedvalueerror(
    tvm,
):
    """test to raise the exception when value of permission is not passed as defined"""
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.credentials, '_permissions_constructor')([('user', 32, 'someone')])


def test_credentials_permissions_constructor_dict_permission_type_typeerror(tvm):
    """test to raise the exception when type of permission type is not passed as defined"""

    with pytest.raises(TypeError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [{'type': 1, 'permissions': 32, 'grantee_uuid': str(uuid.uuid4())}]
        )


def test_credentials_permissions_constructor_dict_permission_type_unexpectedvalueerror(
    tvm,
):
    """test to raise the exception when value of permission type is not passed as defined"""
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [{'type': 'nope', 'permissions': 32, 'grantee_uuid': str(uuid.uuid4())}]
        )


def test_credentials_permissions_constructor_dict_permission_permission_unexpectedvalueerror(
    tvm,
):
    """test to raise the exception when value of permission is not passed as defined"""
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [{'type': 'user', 'permissions': 256, 'grantee_uuid': str(uuid.uuid4())}]
        )


def test_credentials_permissions_constructor_dict_permission_uuid_typeerror(tvm):
    """test to raise the exception when type of uuid is not passed as defined"""
    with pytest.raises(TypeError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [{'type': 'user', 'permissions': 32, 'grantee_uuid': 1}]
        )


def test_credentials_permissions_constructor_dict_permission_uuid_unexpectedvalueerror(
    tvm,
):
    """test to raise the exception when value of uuid is not passed as defined"""
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.credentials, '_permissions_constructor')(
            [{'type': 'user', 'permissions': 32, 'grantee_uuid': 'someone'}]
        )


def test_credentials_permissions_constructor_tuple_success(tvm):
    """test to check the type of permission constructor as tuple"""

    test_id = str(uuid.uuid4())
    resp = getattr(tvm.credentials, '_permissions_constructor')([('user', 32, test_id)])
    assert resp == [{'type': 'user', 'permissions': 32, 'grantee_uuid': test_id}]
    resp = getattr(tvm.credentials, '_permissions_constructor')(
        [('user', 'use', test_id)]
    )
    assert resp == [{'type': 'user', 'permissions': 32, 'grantee_uuid': test_id}]


def test_credentials_permissions_constructor_dict_success(tvm):
    """test to check the type of permission constructor as dict"""
    test_id = str(uuid.uuid4())
    resp = getattr(tvm.credentials, '_permissions_constructor')(
        [{'type': 'user', 'permissions': 32, 'grantee_uuid': test_id}]
    )
    assert resp == [{'type': 'user', 'permissions': 32, 'grantee_uuid': test_id}]


@pytest.fixture
def cred():
    """fixture credential"""
    return '5d218473-39c1-4dff-b5af-cc6d68083404'


def test_credentials_create_cred_name_typeerror(tvm):
    """test to raise the exception when type of credential name  is not as defined"""
    with pytest.raises(TypeError):
        tvm.credentials.create(1, 'something')


def test_credentials_create_cred_type_typeerror(tvm):
    """test to raise the exception when type of credential type is not as defined"""
    with pytest.raises(TypeError):
        tvm.credentials.create('something', 1)


def test_credentials_create_description_typeerror(tvm):
    """test to raise the exception when type of description is not as defined"""
    with pytest.raises(TypeError):
        tvm.credentials.create('something', 'something', 1)


@responses.activate
def test_credentials_create_success(tvm, cred):
    """test to create the credential"""
    responses.add(responses.POST, 'https://nourl/credentials', json={'uuid': cred})
    cred = tvm.credentials.create(
        'Example Cred',
        'SSH',
        username='root',
        password='something',
        auth_method='password',
        elevate_privileges_with='Nothing',
        custom_password_prompt='',
    )
    single(cred, 'uuid')


@responses.activate
def test_credentials_delete_success(tvm, cred):
    """test to delete the credential"""
    responses.add(
        responses.DELETE,
        'https://nourl/credentials/5d218473-39c1-4dff-b5af-cc6d68083404',
        json={'deleted': True},
    )
    tvm.credentials.delete(cred)


@responses.activate
def test_credentials_edit_success(tvm, cred):
    """test to edit the credentials"""
    responses.add(
        responses.GET,
        'https://nourl/credentials/5d218473-39c1-4dff-b5af-cc6d68083404',
        json=CREDENTIALS,
    )
    responses.add(
        responses.PUT,
        'https://nourl/credentials/5d218473-39c1-4dff-b5af-cc6d68083404',
        json={'updated': True},
    )
    creds = tvm.credentials.edit(cred, cred_name='updated cred')
    assert isinstance(creds, bool)


@responses.activate
def test_credentials_details_success(tvm, cred):
    """test to get the details of the credentials"""
    responses.add(
        responses.GET,
        'https://nourl/credentials/5d218473-39c1-4dff-b5af-cc6d68083404',
        json=CREDENTIALS,
    )
    creds = tvm.credentials.details(cred)
    assert isinstance(creds, dict)
    check(creds, 'name', str)
    check(creds, 'description', str)
    check(creds, 'category', dict)
    check(creds['category'], 'id', str)
    check(creds['category'], 'name', str)
    check(creds, 'type', dict)
    check(creds['type'], 'id', str)
    check(creds['type'], 'name', str)
    check(creds, 'ad_hoc', bool)
    check(creds, 'user_permissions', int)
    check(creds, 'settings', dict)
    for setting in creds['settings']:
        check(creds['settings'], setting, str)
    check(creds, 'permissions', list)
    for permission in creds['permissions']:
        check(permission, 'grantee_uuid', 'uuid')
        check(permission, 'type', str)
        check(permission, 'permissions', int)
        check(permission, 'name', str)


def test_credentials_list_offset_typeerror(tvm):
    """test to raise the exception when type of offset is not as defined"""
    with pytest.raises(TypeError):
        tvm.credentials.list(offset='nope')


def test_credentials_list_limit_typeerror(tvm):
    """test to raise the exception when type of limit is not as defined"""
    with pytest.raises(TypeError):
        tvm.credentials.list(limit='nope')


def test_credentials_list_sort_field_typeerror(tvm):
    """test to raise the exception when type of sort_field are not as defined"""
    with pytest.raises(TypeError):
        tvm.credentials.list(sort=((1, 'asc'),))


def test_credentials_list_sort_direction_typeerror(tvm):
    """test to raise the exception when type of sort direction are not as defined"""
    with pytest.raises(TypeError):
        tvm.credentials.list(sort=(('uuid', 1),))


def test_credentials_list_sort_direction_unexpectedvalue(tvm):
    """
    test to raise the exception when value of sort_direction are not as defined
    """
    with pytest.raises(UnexpectedValueError):
        tvm.credentials.list(sort=(('uuid', 'nope'),))


def test_credentials_list_filter_name_typeerror(tvm):
    """
    test to raise the exception when type of filter name are not as defined
    """
    with pytest.raises(TypeError):
        tvm.credentials.list((1, 'match', 'win'))


def test_credentials_list_filter_operator_typeerror(tvm):
    """
    test to raise the exception when type of filter operator are not as defined
    """
    with pytest.raises(TypeError):
        tvm.credentials.list(('name', 1, 'win'))


def test_credentials_list_filter_value_typeerror(tvm):
    """
    test to raise the exception when type of filter value are not as defined
    """
    with pytest.raises(TypeError):
        tvm.credentials.list(('name', 'match', 1))


def test_credentials_list_filter_type_typeerror(tvm):
    """
    test to raise the exception when type of filter type are not as defined
    """
    with pytest.raises(TypeError):
        tvm.credentials.list(filter_type=1)


def test_credentials_list_wildcard_typeerror(tvm):
    """
    test to raise the exception when type of wildcard are not as defined
    """
    with pytest.raises(TypeError):
        tvm.credentials.list(wildcard=1)


def test_credentials_list_wildcard_fields_typeerror(tvm):
    """
    test to raise the exception when type of wildcard_fields are not as defined
    """
    with pytest.raises(TypeError):
        tvm.credentials.list(wildcard_fields='nope')


@responses.activate
def test_credentials_list(tvm):
    """
    test to get credentials list
    """
    responses.add(
        responses.GET,
        'https://nourl/credentials',
        json={
            'credentials': [
                {
                    'uuid': '91107402-dc87-4779-918d-ab5f76deb3a9',
                    'name': 'Root',
                    'description': '',
                    'category': {'id': 'Host', 'name': 'Host'},
                    'type': {'id': 'SSH', 'name': 'SSH'},
                    'created_date': 1538595123,
                    'created_by': {'id': 3, 'display_name': 'test_admin@pytenable.io'},
                    'last_used_by': {
                        'id': 3,
                        'display_name': 'test_admin@pytenable.io',
                    },
                    'permission': 64,
                    'user_permissions': 64,
                }
            ],
            'pagination': {
                'total': 1,
                'limit': 50,
                'offset': 0,
                'sort': [{'name': 'created_date', 'order': 'desc'}],
            },
        },
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '0'})],
    )
    count = 0
    credentials = tvm.credentials.list()
    for cred in credentials:
        count += 1
        assert isinstance(cred, dict)
        check(cred, 'uuid', str)
        check(cred, 'name', str)
        check(cred, 'description', str)
        check(cred, 'category', dict)
        check(cred['category'], 'id', str)
        check(cred['category'], 'name', str)
        check(cred, 'type', dict)
        check(cred['type'], 'id', str)
        check(cred['type'], 'name', str)
        check(cred, 'created_date', int)
        check(cred, 'created_by', dict)
        check(cred['created_by'], 'id', int)
        check(cred['created_by'], 'display_name', str)
        check(cred, 'last_used_by', dict)
        check(cred['last_used_by'], 'id', int, allow_none=True)
        check(cred['last_used_by'], 'display_name', str, allow_none=True)
        check(cred, 'permission', int)
        check(cred, 'user_permissions', int)
    assert count == credentials.total


def test_credentials_upload_type_error(tvm):
    """
    test to raise error when the type param is not set.
    """

    # Create a BytesIO object
    file = io.BytesIO(b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64')

    with pytest.raises(TypeError):
        tvm.credentials.upload(file)


def test_credentials_upload_should_fail_on_unsupported_type(tvm):
    """
    test to raise error when the type param is not set.
    """

    # Create a BytesIO object
    file = io.BytesIO(b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64')

    with pytest.raises(UnexpectedValueError):
        tvm.credentials.upload(file, 'some_type')


@responses.activate
def test_credentials_upload_should_succeed(tvm):
    """
    test to succeed only when all the values are set properly.
    """
    responses.add(
        responses.POST,
        'https://nourl/credentials/files',
        json={'fileuploaded': 'Filedata_24d3c310-49a3-4adb-a8cd-748a9192f844'},
        match=[matchers.query_param_matcher({'fileType': 'pem'})],
    )

    # Create a BytesIO object
    file = io.BytesIO(b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64')
    uploaded_file = tvm.credentials.upload(file, 'pem')
    assert type(uploaded_file) is str


def test_credentials_permissions_constructor_typeerror(tvm):
    """
    test to raise the exception when the required type of variable is not passed
    """
    with pytest.raises(TypeError):
        getattr(tvm.credentials, '_permissions_constructor')('string')


@responses.activate
def test_credentials_types_success(tvm):
    """
    test to check the types of credentials
    """
    responses.add(
        responses.GET,
        'https://nourl/credentials/types',
        json={
            'credentials': [
                {
                    'id': 'API Gateway',
                    'category': 'API Gateway',
                    'default_expand': False,
                    'types': [
                        {
                            'id': 'IBM DataPower Gateway',
                            'name': 'IBM DataPower Gateway',
                            'max': 1,
                            'configuration': [
                                {
                                    'type': 'file',
                                    'name': 'Client Certificate',
                                    'hint': 'PEM formatted certificate.',
                                    'id': 'datapower_client_cert',
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    )
    resp = tvm.credentials.types()
    assert isinstance(resp, list)
    for data in resp:
        check(data, 'id', str)
        check(data, 'category', str, allow_none=True)
        check(data, 'default_expand', bool, allow_none=True)
        check(data, 'types', list, allow_none=True)
        for each_type in data.get('types'):
            check(each_type, 'id', str, allow_none=True)
            check(each_type, 'name', str, allow_none=True)
            check(each_type, 'max', int, allow_none=True)
            check(each_type, 'configuration', list, allow_none=True)
            for config in each_type.get('configuration'):
                check(config, 'type', str)
                check(config, 'name', str)
                if 'hint' in config.keys():
                    check(config, 'hint', str, allow_none=True)
                check(config, 'id', str)


@responses.activate
def test_credentials_list_fields(tvm, scan):
    """
    test to check the list of credentials and their types
    """
    responses.add(
        responses.GET,
        'https://nourl/credentials',
        json={
            'credentials': [],
            'pagination': {
                'total': 0,
                'limit': 45,
                'offset': 2,
                'sort': [{'name': 'created_date', 'order': 'desc'}],
            },
        },
        match=[
            matchers.query_param_matcher(
                {
                    'referrer_owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                    'ft': 'or',
                    'w': 'match',
                    'wf': 'name',
                    'limit': '45',
                    'offset': '2',
                }
            )
        ],
    )
    count = 0
    credentials = tvm.credentials.list(
        filter_type='or',
        limit=45,
        offset=2,
        wildcard='match',
        wildcard_fields=['name'],
        owner_uuid=scan['owner_uuid'],
    )
    for creds in credentials:
        count += 1
        assert isinstance(creds, dict)
        check(creds, 'uuid', str)
        check(creds, 'name', str)
        check(creds, 'description', str)
        check(creds, 'category', dict)
        check(creds['category'], 'id', str)
        check(creds['category'], 'name', str)
        check(creds, 'type', dict)
        check(creds['type'], 'id', str)
        check(creds['type'], 'name', str)
        check(creds, 'created_date', int)
        check(creds, 'created_by', dict)
        check(creds['created_by'], 'id', int)
        check(creds['created_by'], 'display_name', str)
        check(creds, 'last_used_by', dict)
        check(creds['last_used_by'], 'id', int, allow_none=True)
        check(creds['last_used_by'], 'display_name', str, allow_none=True)
        check(creds, 'permission', int)
        check(creds, 'user_permissions', int)
    assert count == credentials.total


@responses.activate
def test_credentials_edit_with_permissions(tvm, cred):
    """test to edit with permissions parameter in the credentials"""
    responses.add(
        responses.GET,
        'https://nourl/credentials/f07267e2-2994-4293-900a-8acc9adaacd4',
        json={
            'name': 'updated cred',
            'description': '',
            'category': {'id': 'Host', 'name': 'Host'},
            'type': {'id': 'Windows', 'name': 'Windows'},
            'ad_hoc': False,
            'user_permissions': 64,
            'settings': {
                'domain': '',
                'username': 'administrator',
                'auth_method': 'Password',
                'password': '********',
            },
            'permissions': [
                {
                    'grantee_uuid': 'e1b94c27-9dca-4367-b75f-ea6c37deaa0f',
                    'type': 'user',
                    'permissions': 64,
                    'name': 'triage_musikaar@tenable.com',
                },
                {
                    'grantee_uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'user',
                    'permissions': 64,
                    'name': None,
                },
            ],
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/credentials/f07267e2-2994-4293-900a-8acc9adaacd4',
        json={'updated': True},
    )
    creds = tvm.credentials.edit(
        'f07267e2-2994-4293-900a-8acc9adaacd4',
        cred_name='updated cred',
        permissions=[
            {
                'grantee_uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'user',
                'permissions': 64,
                'name': 'test_admin@pytenable.io',
            }
        ],
    )
    assert isinstance(creds, bool)
