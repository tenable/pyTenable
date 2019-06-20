from tenable.errors import *
from ..checker import check, single
import uuid, pytest

def guser():
    return '{}@pytenable.io'.format(uuid.uuid4())

def gpass():
    return '{}Tt!'.format(uuid.uuid4())

@pytest.mark.vcr()
def test_users_create_username_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(False, gpass(), 1)

@pytest.mark.vcr()
def test_users_create_password_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), False, 1)

@pytest.mark.vcr()
def test_users_create_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 'nope')

@pytest.mark.vcr()
def test_users_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, name=1)

@pytest.mark.vcr()
def test_users_create_email_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, email=1)

@pytest.mark.vcr()
def test_users_create_account_type_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, account_type=False)

@pytest.mark.vcr()
def test_users_create_permissionserror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.users.create(guser(), gpass(), 16)

@pytest.mark.vcr()
def test_users_create(api, user):
    assert isinstance(user, dict)
    check(user, 'id', int)
    check(user, 'username', str)
    check(user, 'name', str)
    check(user, 'email', str)
    check(user, 'permissions', int)
    check(user, 'type', str)
    check(user, 'login_fail_count', int)
    check(user, 'login_fail_total', int)
    check(user, 'enabled', bool)
    check(user, 'uuid_id', 'uuid')

@pytest.mark.vcr()
def test_users_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.delete('False')

@pytest.mark.vcr()
def test_users_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.delete(0)

@pytest.mark.vcr()
def test_users_delete_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.delete(user['id'])

@pytest.mark.vcr()
def test_users_delete(api, user):
    api.users.delete(user['id'])
    assert user['id'] not in [u['id'] for u in api.users.list()]

def test_users_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.details('nope')

@pytest.mark.vcr()
def test_users_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.details(0)

@pytest.mark.vcr()
def test_users_details(api, user):
    u = api.users.details(user['id'])
    assert isinstance(user, dict)
    check(u, 'id', int)
    check(u, 'username', str)
    check(u, 'name', str)
    check(u, 'email', str)
    check(u, 'permissions', int)
    check(u, 'type', str)
    check(u, 'login_fail_count', int)
    check(u, 'login_fail_total', int)
    check(u, 'enabled', bool)
    check(u, 'uuid_id', 'uuid')

@pytest.mark.vcr()
def test_users_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit('nope')

@pytest.mark.vcr()
def test_users_edit_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, permissions='nope')

@pytest.mark.vcr()
def test_users_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, name=1)

@pytest.mark.vcr()
def test_users_edit_email_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, email=1)

@pytest.mark.vcr()
def test_users_edit_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, enabled='nope')

@pytest.mark.vcr()
def test_users_edit_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.edit(0, email=guser())

@pytest.mark.vcr()
def test_users_edit_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.edit(user['id'], name=str(uuid.uuid4()))

@pytest.mark.vcr()
def test_users_edit(api, user):
    u = api.users.edit(user['id'], name='MODDED NAME')
    assert isinstance(user, dict)
    check(u, 'id', int)
    check(u, 'username', str)
    check(u, 'name', str)
    check(u, 'email', str)
    check(u, 'permissions', int)
    check(u, 'type', str)
    check(u, 'login_fail_count', int)
    check(u, 'login_fail_total', int)
    check(u, 'enabled', bool)
    check(u, 'uuid_id', 'uuid')
    assert u['name'] == 'MODDED NAME'

@pytest.mark.vcr()
def test_users_enabled_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.enabled('nope', False)

@pytest.mark.vcr()
def test_users_enabled_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.users.enabled(1, 'nope')

@pytest.mark.vcr()
def test_users_enabled_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.enabled(0, False)

@pytest.mark.vcr()
def test_users_enabled_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.enabled(user['id'], False)

@pytest.mark.vcr()
def test_users_enabled(api, user):
    disabled = api.users.enabled(user['id'], False)
    assert isinstance(disabled, dict)
    assert disabled['enabled'] == False

@pytest.mark.vcr()
def test_users_two_factor_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor('nope', False, False)

@pytest.mark.vcr()
def test_users_two_factor_email_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor(0, False, 'nope')

@pytest.mark.vcr()
def test_users_two_factor_sms_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor('nope', False)

@pytest.mark.vcr()
def test_users_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor(False, False, 8675309)

@pytest.mark.vcr()
@pytest.mark.xfail(raises=InvalidInputError)
def test_users_two_factor(api, user):
    api.users.two_factor(user['id'], False, False)

@pytest.mark.vcr()
@pytest.mark.vcr()
def test_users_enable_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.users.enable_two_factor(False)

@pytest.mark.vcr()
@pytest.mark.skip(reason="Don't want to enable two-facor on the user.")
def test_users_enable_two_factor(api):
    api.users.enable_two_factor('867-5309')

@pytest.mark.vcr()
def test_users_verify_two_factor_code_typeerror(api):
    with pytest.raises(TypeError):
        api.users.verify_two_factor(False)

@pytest.mark.vcr()
@pytest.mark.skip(reason="Don't want to enable two-facor on the user.")
def test_users_verify_two_factor(api):
    api.users.verify_two_factor(False)

@pytest.mark.vcr()
def test_users_impersonate_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.impersonate(1)
        api.session.restore()

@pytest.mark.vcr()
def test_users_impersonate_notfounderror(api):
    with pytest.raises(PermissionError):
        api.users.impersonate(guser())
        api.session.details()
        api.session.restore()

@pytest.mark.vcr()
def test_users_impersonate_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.impersonate(user['username'])
        stdapi.session.details()
        stdapi.session.restore()

@pytest.mark.vcr()
def test_users_impersonate(api, user):
    api.users.impersonate(user['username'])
    assert api.session.details()['username'] == user['username']
    api.session.restore()
    assert api.session.details()['username'] != user['username']

@pytest.mark.vcr()
def test_users_list_users(api, user):
    users = api.users.list()
    assert isinstance(users, list)
    assert user['id'] in [u['id']for u in users]

@pytest.mark.vcr()
def test_users_change_password_orig_typeerror(api):
    with pytest.raises(TypeError):
        api.users.change_password(0, False, 'nope')

@pytest.mark.vcr()
def test_users_change_password_new_typeerror(api):
    with pytest.raises(TypeError):
        api.users.change_password(0, 'nope', False)

@pytest.mark.vcr()
def test_users_change_password_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.change_password('fail', 'nope', 'nope')

@pytest.mark.vcr()
def test_users_change_password_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.change_password(0, 'nope', 'nope')

@pytest.mark.vcr()
def test_users_change_password_permissionserror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.change_password(user['id'], 'nope', 'nope')

@pytest.mark.vcr()
def test_users_change_password(api):
    password = gpass()
    user = api.users.create(guser(), password, 16)
    api.users.change_password(user['id'], password, gpass())
    api.users.delete(user['id'])