from tenable.errors import *
from ..checker import check, single
import pytest

def test_users_constructor_role_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(role='one')

def test_users_constructor_group_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(group='one')

def test_users_constructor_org_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(org='one')

def test_users_constructor_responsibility_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(responsibility='one')

def test_users_constructor_keys_typeerror(sc):
    keys = [
            'ldapUsername', 'username', 'firstname', 'lastname', 'title',
            'email', 'address', 'city', 'state', 'country', 'phone', 'fax',
            'fingerprint', 'status'
        ]
    for k in keys:
        with pytest.raises(TypeError):
            sc.users._constructor(*{k: 1})

def test_users_constructor_is_locked_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(is_locked='yup')

def test_users_constructor_auth_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(auth_type=1)

def test_users_constructor_auth_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.users._constructor(auth_type='something')

def test_users_constructor_email_notice_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(email_notice=1)

def test_users_constructor_email_notice_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.users._constructor(email_notice='something')

def test_users_constructor_timezone_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(timezone=1)

def test_users_constructor_update_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(update_password='nope')

def test_users_constructor_managed_usergroups_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(managed_usergroups=1)

def test_users_constructor_managed_usergroups_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(managed_usergroups=['one'])

def test_users_constructor_managed_userobjs_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(managed_userobjs=1)

def test_users_constructor_managed_userobjs_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(managed_userobjs=['one'])

def test_users_constructor_def_reports_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(default_reports='nope')

def test_users_constructor_def_dashboards_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(default_dashboards='nope')

def test_users_constructor_def_reportcards_typeerror(sc):
    with pytest.raises(TypeError):
        sc.users._constructor(default_reportcards='nope')

def test_users_constructor_success(sc):
    user = sc.users._constructor(
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
        default_reports=False,
        default_dashboards=False,
        default_reportcards=False
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
        'importReports': 'false',
        'importDashboards': 'false',
        'importARCs': 'false'
    }

@pytest.fixture
def user(request, sc, vcr):
    with vcr.use_cassette('test_users_create_success'):
        user = sc.users.create('user', 'password', 2, group=0)
    def teardown():
        try:
            with vcr.use_cassette('test_users_delete_success'):
                sc.users.delete(int(user['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return user

@pytest.mark.vcr()
def test_users_create_success(sc, user):
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
    for i in user['managedUsersGroups']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(user, 'managedObjectsGroups', list)
    for i in user['managedObjectsGroups']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(user, 'preferences', list)
    for i in user['preferences']:
        check(i, 'name', str)
        check(i, 'value', str)
        check(i, 'tag', str)
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
def test_users_edit_success(sc, user):
    u = sc.users.edit(int(user['id']), username='newusername')
    assert isinstance(u, dict)
    check(u, 'id', str)
    check(u, 'status', str)
    check(u, 'ldapUsername', str)
    check(u, 'firstname', str)
    check(u, 'lastname', str)
    check(u, 'title', str)
    check(u, 'email', str)
    check(u, 'address', str)
    check(u, 'city', str)
    check(u, 'state', str)
    check(u, 'country', str)
    check(u, 'phone', str)
    check(u, 'createdTime', str)
    check(u, 'modifiedTime', str)
    check(u, 'lastLogin', str)
    check(u, 'lastLoginIP', str)
    check(u, 'mustChangePassword', str)
    check(u, 'locked', str)
    check(u, 'failedLogins', str)
    check(u, 'authType', str)
    check(u, 'fingerprint', str, allow_none=True)
    check(u, 'password', str)
    check(u, 'managedUsersGroups', list)
    for i in u['managedUsersGroups']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(u, 'managedObjectsGroups', list)
    for i in u['managedObjectsGroups']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(u, 'preferences', list)
    for i in u['preferences']:
        check(i, 'name', str)
        check(i, 'value', str)
        check(i, 'tag', str)
    check(u, 'canUse', bool)
    check(u, 'canManage', bool)
    check(u, 'role', dict)
    check(u['role'], 'id', str)
    check(u['role'], 'name', str)
    check(u['role'], 'description', str)
    check(u, 'responsibleAsset', dict)
    check(u['responsibleAsset'], 'id', int)
    check(u['responsibleAsset'], 'name', str)
    check(u['responsibleAsset'], 'description', str)
    check(u, 'group', dict)
    check(u['group'], 'id', str)
    check(u['group'], 'name', str)
    check(u['group'], 'description', str)
    check(u, 'ldap', dict)
    check(u['ldap'], 'id', int)
    check(u['ldap'], 'name', str)
    check(u['ldap'], 'description', str)

@pytest.mark.vcr()
def test_users_details_success(sc, user):
    u = sc.users.details(int(user['id']))
    assert isinstance(u, dict)
    check(u, 'id', str)
    check(u, 'status', str)
    check(u, 'ldapUsername', str)
    check(u, 'firstname', str)
    check(u, 'lastname', str)
    check(u, 'title', str)
    check(u, 'email', str)
    check(u, 'address', str)
    check(u, 'city', str)
    check(u, 'state', str)
    check(u, 'country', str)
    check(u, 'phone', str)
    check(u, 'createdTime', str)
    check(u, 'modifiedTime', str)
    check(u, 'lastLogin', str)
    check(u, 'lastLoginIP', str)
    check(u, 'mustChangePassword', str)
    check(u, 'locked', str)
    check(u, 'failedLogins', str)
    check(u, 'authType', str)
    check(u, 'fingerprint', str, allow_none=True)
    check(u, 'password', str)
    check(u, 'managedUsersGroups', list)
    for i in u['managedUsersGroups']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(u, 'managedObjectsGroups', list)
    for i in u['managedObjectsGroups']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(u, 'preferences', list)
    for i in u['preferences']:
        check(i, 'name', str)
        check(i, 'value', str)
        check(i, 'tag', str)
    check(u, 'canUse', bool)
    check(u, 'canManage', bool)
    check(u, 'role', dict)
    check(u['role'], 'id', str)
    check(u['role'], 'name', str)
    check(u['role'], 'description', str)
    check(u, 'responsibleAsset', dict)
    check(u['responsibleAsset'], 'id', int)
    check(u['responsibleAsset'], 'name', str)
    check(u['responsibleAsset'], 'description', str)
    check(u, 'group', dict)
    check(u['group'], 'id', str)
    check(u['group'], 'name', str)
    check(u['group'], 'description', str)
    check(u, 'ldap', dict)
    check(u['ldap'], 'id', int)
    check(u['ldap'], 'name', str)
    check(u['ldap'], 'description', str)

@pytest.mark.vcr()
def test_users_delete_success(sc, user):
    sc.users.delete(int(user['id']))