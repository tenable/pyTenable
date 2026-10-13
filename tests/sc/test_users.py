"""
test file for testing various scenarios in security center's users functionality
"""

import pytest
from responses import matchers
import responses
from responses.matchers import json_params_matcher
from tenable.sc import TenableSC
from tenable.errors import UnexpectedValueError
from ..checker import check


def test_users_constructor_role_typeerror(tsc):
    """
    test users constructor for role type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(role='one')


def test_users_constructor_group_typeerror(tsc):
    """
    test users constructor for group type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(group='one')


def test_users_constructor_org_typeerror(tsc):
    """
    test users constructor for org type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(org='one')


def test_users_constructor_responsibility_typeerror(tsc):
    """
    test users constructor for responsibility type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(responsibility='one')


def test_users_constructor_ldap_id(tsc):
    """
    test users constructor for 'ldap id' success
    """
    kwargs = tsc.users._constructor(ldap_id=1)
    check(kwargs, 'ldap', object)
    assert kwargs.get('ldap')['id'] == 1


def test_users_constructor_keys_typeerror(tsc):
    """
    test users constructor for keys type error
    """
    keys = [
        'ldapUsername',
        'username',
        'firstname',
        'lastname',
        'title',
        'email',
        'address',
        'city',
        'state',
        'country',
        'phone',
        'fax',
        'fingerprint',
        'status',
    ]
    for key in keys:
        with pytest.raises(TypeError):
            tsc.users._constructor(*{key: 1})


def test_users_constructor_is_locked_typeerror(tsc):
    """
    test users constructor for 'is locked' type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(is_locked='yup')


def test_users_constructor_auth_type_typeerror(tsc):
    """
    test users constructor for 'auth type' type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(auth_type=1)


def test_users_constructor_auth_type_unexpectedvalueerror(tsc):
    """
    test users constructor for auth type unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.users._constructor(auth_type='something')


def test_users_constructor_email_notice_typeerror(tsc):
    """
    test users constructor for email notice type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(email_notice=1)


def test_users_constructor_email_notice_unexpectedvalueerror(tsc):
    """
    test users constructor for email notice unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.users._constructor(email_notice='something')


def test_users_constructor_timezone_typeerror(tsc):
    """
    test users constructor for timezone type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(timezone=1)


def test_users_constructor_update_password_typeerror(tsc):
    """
    test users constructor for 'update password' type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(update_password='nope')


def test_users_constructor_managed_usergroups_typeerror(tsc):
    """
    test users constructor for 'manage user groups' type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(managed_usergroups=1)


def test_users_constructor_managed_usergroups_item_typeerror(tsc):
    """
    test users constructor for 'manage user groups item' type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(managed_usergroups=['one'])


def test_users_constructor_managed_userobjs_typeerror(tsc):
    """
    test users constructor for 'manage user objs' type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(managed_userobjs=1)


def test_users_constructor_managed_userobjs_item_typeerror(tsc):
    """
    test users constructor for 'manage user objs item' type error
    """
    with pytest.raises(TypeError):
        tsc.users._constructor(managed_userobjs=['one'])


def test_users_constructor_create_default_objects(tsc):
    assert tsc.users._constructor(default_objects=True) == {
        'createDefaultObjects': 'true'
    }
    assert tsc.users._constructor(default_objects=False) == {
        'createDefaultObjects': 'false'
    }
    assert tsc.users._constructor() == {'createDefaultObjects': 'false'}
    assert tsc.users._constructor(createDefaultObjects='true') == {
        'createDefaultObjects': 'true'
    }


def test_users_constructor_success(tsc):
    """
    test users constructor for success
    """
    user = tsc.users._constructor(
        username='jsmith',
        password='notmypassword',
        role=1,
        group=1,
        org=1,
        auth_type='tns',
        responsibility=0,
        firstname='John',
        lastname='Smith',
        title='Vuln Vanquisher',
        is_locked=False,
        email_notice='both',
        timezone='Americas/Chicago',
        update_password=True,
        managed_usergroups=[1],
        managed_userobjs=[1],
        default_objects=True,
    )
    assert isinstance(user, dict)
    assert user == {
        'roleID': 1,
        'groupID': 1,
        'orgID': 1,
        'responsibleAssetID': 0,
        'username': 'jsmith',
        'firstname': 'John',
        'lastname': 'Smith',
        'title': 'Vuln Vanquisher',
        'password': 'notmypassword',
        'locked': 'false',
        'authType': 'tns',
        'emailNotice': 'both',
        'preferences': [
            {'name': 'timezone', 'tag': 'system', 'value': 'Americas/Chicago'}
        ],
        'mustChangePassword': 'true',
        'managedUsersGroups': [{'id': 1}],
        'managedObjectsGroups': [{'id': 1}],
        'createDefaultObjects': 'true',
    }


@pytest.fixture
def user():
    """
    test fixture for user
    """
    return {
        'id': '4',
        'status': '0',
        'username': 'user',
        'firstname': '',
        'lastname': '',
        'title': '',
        'email': '',
        'address': '',
        'city': '',
        'state': '',
        'country': '',
        'phone': '',
        'fax': '',
        'createdTime': '1554493356',
        'modifiedTime': '1554493356',
        'lastLogin': '0',
        'lastLoginIP': '',
        'mustChangePassword': 'false',
        'locked': 'false',
        'failedLogins': '0',
        'authType': 'tns',
        'fingerprint': None,
        'password': 'SET',
        'ldapUsername': '',
        'canUse': True,
        'canManage': True,
    }


@responses.activate
def test_users_create_success(tsc):
    """
    test users create for success
    """
    responses.post(
        'https://nourl/rest/user',
        json={
            'type': 'regular',
            'response': {
                'id': '4',
                'status': '0',
                'username': 'user',
                'firstname': '',
                'lastname': '',
                'title': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'createdTime': '1554493356',
                'modifiedTime': '1554493356',
                'lastLogin': '0',
                'lastLoginIP': '',
                'mustChangePassword': 'false',
                'locked': 'false',
                'failedLogins': '0',
                'authType': 'tns',
                'fingerprint': None,
                'password': 'SET',
                'ldapUsername': '',
                'managedUsersGroups': [],
                'managedObjectsGroups': [],
                'preferences': [
                    {'name': 'timezone', 'value': 'America/New_York', 'tag': 'system'}
                ],
                'canUse': True,
                'canManage': True,
                'role': {
                    'id': '2',
                    'name': 'Security Manager',
                    'description': 'The Security Manager role has full access to all actions at the organization level. A Security Manager has the ability t',
                },
                'responsibleAsset': {'id': -1, 'name': '', 'description': ''},
                'group': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'ldap': {'id': -1, 'name': '', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1554493355,
        },
    )
    user = tsc.users.create('user', 'password', 2, group=0)
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'status', str)
    check(user, 'ldapUsername', str)
    check(user, 'firstname', str)
    check(user, 'lastname', str)
    check(user, 'title', str)
    check(user, 'email', str)
    check(user, 'address', str)
    check(user, 'city', str)
    check(user, 'state', str)
    check(user, 'country', str)
    check(user, 'phone', str)
    check(user, 'createdTime', str)
    check(user, 'modifiedTime', str)
    check(user, 'lastLogin', str)
    check(user, 'lastLoginIP', str)
    check(user, 'mustChangePassword', str)
    check(user, 'locked', str)
    check(user, 'failedLogins', str)
    check(user, 'authType', str)
    check(user, 'fingerprint', str, allow_none=True)
    check(user, 'password', str)
    check(user, 'managedUsersGroups', list)
    for user_group in user['managedUsersGroups']:
        check(user_group, 'id', str)
        check(user_group, 'name', str)
        check(user_group, 'description', str)
    check(user, 'managedObjectsGroups', list)
    for object_group in user['managedObjectsGroups']:
        check(object_group, 'id', str)
        check(object_group, 'name', str)
        check(object_group, 'description', str)
    check(user, 'preferences', list)
    for preference in user['preferences']:
        check(preference, 'name', str)
        check(preference, 'value', str)
        check(preference, 'tag', str)
    check(user, 'canUse', bool)
    check(user, 'canManage', bool)
    check(user, 'role', dict)
    check(user['role'], 'id', str)
    check(user['role'], 'name', str)
    check(user['role'], 'description', str)
    check(user, 'responsibleAsset', dict)
    check(user['responsibleAsset'], 'id', int)
    check(user['responsibleAsset'], 'name', str)
    check(user['responsibleAsset'], 'description', str)
    check(user, 'group', dict)
    check(user['group'], 'id', str)
    check(user['group'], 'name', str)
    check(user['group'], 'description', str)
    check(user, 'ldap', dict)
    check(user['ldap'], 'id', int)
    check(user['ldap'], 'name', str)
    check(user['ldap'], 'description', str)


@responses.activate
def test_users_edit_success(tsc, user):
    """
    test users edit for success
    """
    responses.patch(
        'https://nourl/rest/user/4',
        json={
            'type': 'regular',
            'response': {
                'id': '6',
                'status': '0',
                'username': 'newusername',
                'firstname': '',
                'lastname': '',
                'title': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'createdTime': '1554493701',
                'modifiedTime': '1554493702',
                'lastLogin': '0',
                'lastLoginIP': '',
                'mustChangePassword': 'false',
                'locked': 'false',
                'failedLogins': '0',
                'authType': 'tns',
                'fingerprint': None,
                'password': 'SET',
                'ldapUsername': '',
                'managedUsersGroups': [],
                'managedObjectsGroups': [],
                'preferences': [
                    {'name': 'timezone', 'value': 'America/New_York', 'tag': 'system'}
                ],
                'canUse': True,
                'canManage': True,
                'role': {
                    'id': '2',
                    'name': 'Security Manager',
                    'description': 'The Security Manager role has full access to all actions at the organization level. A Security Manager has the ability t',
                },
                'responsibleAsset': {'id': -1, 'name': '', 'description': ''},
                'group': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'ldap': {'id': -1, 'name': '', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1554493702,
        },
    )
    user = tsc.users.edit(int(user['id']), username='newusername')
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'status', str)
    check(user, 'ldapUsername', str)
    check(user, 'firstname', str)
    check(user, 'lastname', str)
    check(user, 'title', str)
    check(user, 'email', str)
    check(user, 'address', str)
    check(user, 'city', str)
    check(user, 'state', str)
    check(user, 'country', str)
    check(user, 'phone', str)
    check(user, 'createdTime', str)
    check(user, 'modifiedTime', str)
    check(user, 'lastLogin', str)
    check(user, 'lastLoginIP', str)
    check(user, 'mustChangePassword', str)
    check(user, 'locked', str)
    check(user, 'failedLogins', str)
    check(user, 'authType', str)
    check(user, 'fingerprint', str, allow_none=True)
    check(user, 'password', str)
    check(user, 'managedUsersGroups', list)
    for user_group in user['managedUsersGroups']:
        check(user_group, 'id', str)
        check(user_group, 'name', str)
        check(user_group, 'description', str)
    check(user, 'managedObjectsGroups', list)
    for object_group in user['managedObjectsGroups']:
        check(object_group, 'id', str)
        check(object_group, 'name', str)
        check(object_group, 'description', str)
    check(user, 'preferences', list)
    for preference in user['preferences']:
        check(preference, 'name', str)
        check(preference, 'value', str)
        check(preference, 'tag', str)
    check(user, 'canUse', bool)
    check(user, 'canManage', bool)
    check(user, 'role', dict)
    check(user['role'], 'id', str)
    check(user['role'], 'name', str)
    check(user['role'], 'description', str)
    check(user, 'responsibleAsset', dict)
    check(user['responsibleAsset'], 'id', int)
    check(user['responsibleAsset'], 'name', str)
    check(user['responsibleAsset'], 'description', str)
    check(user, 'group', dict)
    check(user['group'], 'id', str)
    check(user['group'], 'name', str)
    check(user['group'], 'description', str)
    check(user, 'ldap', dict)
    check(user['ldap'], 'id', int)
    check(user['ldap'], 'name', str)
    check(user['ldap'], 'description', str)


@responses.activate
def test_users_details_success(tsc, user):
    """
    test users details for success
    """
    responses.get(
        'https://nourl/rest/user/4',
        json={
            'type': 'regular',
            'response': {
                'id': '7',
                'status': '0',
                'username': 'user',
                'firstname': '',
                'lastname': '',
                'title': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'createdTime': '1554493762',
                'modifiedTime': '1554493762',
                'lastLogin': '0',
                'lastLoginIP': '',
                'mustChangePassword': 'false',
                'locked': 'false',
                'failedLogins': '0',
                'authType': 'tns',
                'fingerprint': None,
                'password': 'SET',
                'ldapUsername': '',
                'managedUsersGroups': [],
                'managedObjectsGroups': [],
                'preferences': [
                    {'name': 'timezone', 'value': 'America/New_York', 'tag': 'system'}
                ],
                'canUse': True,
                'canManage': True,
                'role': {
                    'id': '2',
                    'name': 'Security Manager',
                    'description': 'The Security Manager role has full access to all actions at the organization level. A Security Manager has the ability t',
                },
                'responsibleAsset': {'id': -1, 'name': '', 'description': ''},
                'group': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'ldap': {'id': -1, 'name': '', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1554493762,
        },
    )
    user = tsc.users.details(int(user['id']))
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'status', str)
    check(user, 'ldapUsername', str)
    check(user, 'firstname', str)
    check(user, 'lastname', str)
    check(user, 'title', str)
    check(user, 'email', str)
    check(user, 'address', str)
    check(user, 'city', str)
    check(user, 'state', str)
    check(user, 'country', str)
    check(user, 'phone', str)
    check(user, 'createdTime', str)
    check(user, 'modifiedTime', str)
    check(user, 'lastLogin', str)
    check(user, 'lastLoginIP', str)
    check(user, 'mustChangePassword', str)
    check(user, 'locked', str)
    check(user, 'failedLogins', str)
    check(user, 'authType', str)
    check(user, 'fingerprint', str, allow_none=True)
    check(user, 'password', str)
    check(user, 'managedUsersGroups', list)
    for user_group in user['managedUsersGroups']:
        check(user_group, 'id', str)
        check(user_group, 'name', str)
        check(user_group, 'description', str)
    check(user, 'managedObjectsGroups', list)
    for object_group in user['managedObjectsGroups']:
        check(object_group, 'id', str)
        check(object_group, 'name', str)
        check(object_group, 'description', str)
    check(user, 'preferences', list)
    for preference in user['preferences']:
        check(preference, 'name', str)
        check(preference, 'value', str)
        check(preference, 'tag', str)
    check(user, 'canUse', bool)
    check(user, 'canManage', bool)
    check(user, 'role', dict)
    check(user['role'], 'id', str)
    check(user['role'], 'name', str)
    check(user['role'], 'description', str)
    check(user, 'responsibleAsset', dict)
    check(user['responsibleAsset'], 'id', int)
    check(user['responsibleAsset'], 'name', str)
    check(user['responsibleAsset'], 'description', str)
    check(user, 'group', dict)
    check(user['group'], 'id', str)
    check(user['group'], 'name', str)
    check(user['group'], 'description', str)
    check(user, 'ldap', dict)
    check(user['ldap'], 'id', int)
    check(user['ldap'], 'name', str)
    check(user['ldap'], 'description', str)


@responses.activate
def test_users_details_success_for_fields(tsc, user):
    """
    test users details success for fields
    """
    responses.get(
        'https://nourl/rest/user/4',
        json={
            'type': 'regular',
            'response': {'id': '7', 'status': '0', 'username': 'user'},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1554493762,
        },
        match=[matchers.query_param_matcher({'fields': 'id,status,username'})],
    )
    user = tsc.users.details(int(user['id']), fields=['id', 'status', 'username'])
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'status', str)
    check(user, 'username', str)


@responses.activate
def test_users_list_success(tsc):
    """
    test users list for success
    """
    responses.get(
        'https://nourl/rest/user',
        json={
            'type': 'regular',
            'response': {
                'users': [
                    {'id': '7', 'status': '0', 'username': 'user7'},
                    {'id': '8', 'status': '0', 'username': 'user8'},
                ]
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1554493762,
        },
        match=[matchers.query_param_matcher({'fields': 'id,status,username'})],
    )
    users = tsc.users.list(fields=['id', 'status', 'username'])
    for user in users['users']:
        assert isinstance(user, dict)
        check(user, 'id', str)
        check(user, 'status', str)
        check(user, 'username', str)


@responses.activate
def test_users_delete_success(tsc, user):
    """
    test users delete for success
    """
    responses.delete(
        'https://nourl/rest/user/4',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1554493356,
        },
    )
    tsc.users.delete(int(user['id']))


@responses.activate
def test_users_delete_migrate_to():
    responses.get(
        'https://nourl/rest/system', json={'error_code': None, 'response': {}}
    )
    responses.delete(
        'https://nourl/rest/user/1', match=[json_params_matcher({'migrateUserID': 2})]
    )
    sc = TenableSC(url='https://nourl', access_key='something', secret_key='something')
    sc.users.delete(1, 2)
