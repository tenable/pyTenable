'''
test file for testing various scenarios in security center's users functionality
'''
import pytest
import responses
from responses.matchers import query_param_matcher, json_params_matcher
from tenable.sc import TenableSC
from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check


def test_users_constructor_role_typeerror(security_center):
    '''
    test users constructor for role type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(role='one')


def test_users_constructor_group_typeerror(security_center):
    '''
    test users constructor for group type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(group='one')


def test_users_constructor_org_typeerror(security_center):
    '''
    test users constructor for org type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(org='one')


def test_users_constructor_responsibility_typeerror(security_center):
    '''
    test users constructor for responsibility type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(responsibility='one')


def test_users_constructor_ldap_id(security_center):
    '''
    test users constructor for 'ldap id' success
    '''
    kwargs = security_center.users._constructor(ldap_id=1)
    check(kwargs, 'ldap', object)
    assert kwargs.get('ldap')['id'] == 1


def test_users_constructor_keys_typeerror(security_center):
    '''
    test users constructor for keys type error
    '''
    keys = [
        'ldapUsername', 'username', 'firstname', 'lastname', 'title',
        'email', 'address', 'city', 'state', 'country', 'phone', 'fax',
        'fingerprint', 'status'
    ]
    for key in keys:
        with pytest.raises(TypeError):
            security_center.users._constructor(*{key: 1})


def test_users_constructor_is_locked_typeerror(security_center):
    '''
    test users constructor for 'is locked' type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(is_locked='yup')


def test_users_constructor_auth_type_typeerror(security_center):
    '''
    test users constructor for 'auth type' type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(auth_type=1)


def test_users_constructor_auth_type_unexpectedvalueerror(security_center):
    '''
    test users constructor for auth type unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.users._constructor(auth_type='something')


def test_users_constructor_email_notice_typeerror(security_center):
    '''
    test users constructor for email notice type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(email_notice=1)


def test_users_constructor_email_notice_unexpectedvalueerror(security_center):
    '''
    test users constructor for email notice unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.users._constructor(email_notice='something')


def test_users_constructor_timezone_typeerror(security_center):
    '''
    test users constructor for timezone type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(timezone=1)


def test_users_constructor_update_password_typeerror(security_center):
    '''
    test users constructor for 'update password' type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(update_password='nope')


def test_users_constructor_managed_usergroups_typeerror(security_center):
    '''
    test users constructor for 'manage user groups' type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(managed_usergroups=1)


def test_users_constructor_managed_usergroups_item_typeerror(security_center):
    '''
    test users constructor for 'manage user groups item' type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(managed_usergroups=['one'])


def test_users_constructor_managed_userobjs_typeerror(security_center):
    '''
    test users constructor for 'manage user objs' type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(managed_userobjs=1)


def test_users_constructor_managed_userobjs_item_typeerror(security_center):
    '''
    test users constructor for 'manage user objs item' type error
    '''
    with pytest.raises(TypeError):
        security_center.users._constructor(managed_userobjs=['one'])


def test_users_constructor_create_default_objects(security_center):
    assert security_center.users._constructor(default_objects=True) == {'createDefaultObjects': 'true'}
    assert security_center.users._constructor(default_objects=False) == {'createDefaultObjects': 'false'}
    assert security_center.users._constructor() == {'createDefaultObjects': 'false'}
    assert security_center.users._constructor(createDefaultObjects='true') == {'createDefaultObjects': 'true'}



def test_users_constructor_success(security_center):
    '''
    test users constructor for success
    '''
    user = security_center.users._constructor(
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
        'preferences': [{
            'name': 'timezone',
            'tag': 'system',
            'value': 'Americas/Chicago'
        }],
        'mustChangePassword': 'true',
        'managedUsersGroups': [{'id': 1}],
        'managedObjectsGroups': [{'id': 1}],
        'createDefaultObjects': 'true',
    }


@pytest.fixture
def user(request, security_center, vcr):
    '''
    test fixture for user
    '''
    with vcr.use_cassette('test_users_create_success'):
        user = security_center.users.create('user', 'password', 2, group=0)

    def teardown():
        try:
            with vcr.use_cassette('test_users_delete_success'):
                security_center.users.delete(int(user['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return user


@pytest.mark.vcr()
def test_users_create_success(user):
    '''
    test users create for success
    '''
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


@pytest.mark.vcr()
def test_users_edit_success(security_center, user):
    '''
    test users edit for success
    '''
    user = security_center.users.edit(int(user['id']), username='newusername')
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


@pytest.mark.vcr()
def test_users_details_success(security_center, user):
    '''
    test users details for success
    '''
    user = security_center.users.details(int(user['id']))
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


@pytest.mark.vcr()
def test_users_details_success_for_fields(security_center, user):
    '''
    test users details success for fields
    '''
    user = security_center.users.details(int(user['id']), fields=['id', 'status', 'username'])
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'status', str)
    check(user, 'username', str)


@pytest.mark.vcr()
def test_users_list_success(security_center):
    '''
    test users list for success
    '''
    users = security_center.users.list(fields=['id', 'status', 'username'])
    for user in users['users']:
        assert isinstance(user, dict)
        check(user, 'id', str)
        check(user, 'status', str)
        check(user, 'username', str)


@pytest.mark.vcr()
def test_users_delete_success(security_center, user):
    '''
    test users delete for success
    '''
    security_center.users.delete(int(user['id']))


@responses.activate
def test_users_delete_migrate_to():
    responses.get('https://nourl/rest/system', json={'error_code': None, 'response': {}})
    responses.delete(
        'https://nourl/rest/user/1',
        match=[json_params_matcher({
            'migrateUserID': 2
        })]
    )
    sc = TenableSC(url='https://nourl', access_key='something', secret_key='something')
    sc.users.delete(1, 2)
