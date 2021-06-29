'''
test users
'''
import uuid
import pytest
from tenable.errors import PermissionError, NotFoundError, InvalidInputError
from tests.checker import check

def guser():
    '''
    Returns username
    '''
    return '{}@pytenable.io'.format(uuid.uuid4())

def gpass():
    '''
    Returns password
    '''
    return '{}Tt!'.format(uuid.uuid4())

@pytest.mark.vcr()
def test_users_create_username_typeerror(api):
    '''
    test to raise exception when type of username param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.create(False, gpass(), 1)

@pytest.mark.vcr()
def test_users_create_password_typeerror(api):
    '''
    test to raise exception when type of password param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.create(guser(), False, 1)

@pytest.mark.vcr()
def test_users_create_permissions_typeerror(api):
    '''
    test to raise exception when type of permissions param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 'nope')

@pytest.mark.vcr()
def test_users_create_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, name=1)

@pytest.mark.vcr()
def test_users_create_email_typeerror(api):
    '''
    test to raise exception when type of email param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, email=1)

@pytest.mark.vcr()
def test_users_create_account_type_typeerror(api):
    '''
    test to raise exception when type of account_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, account_type=False)

@pytest.mark.vcr()
def test_users_create_permissionserror(stdapi):
    '''
    test to raise exception when standard_user tries to create user.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.create(guser(), gpass(), 16)

@pytest.mark.vcr()
def test_users_create(api, user):
    '''
    test to create user
    '''
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
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.delete('False')

@pytest.mark.vcr()
def test_users_delete_notfounderror(api):
    '''
    test to raise exception when user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.users.delete(0)

@pytest.mark.vcr()
def test_users_delete_permissionerror(stdapi, user):
    '''
    test to raise exception when standard_user tries to delete user.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.delete(user['id'])

@pytest.mark.vcr()
def test_users_delete(api, user):
    '''
    test to delete user
    '''
    api.users.delete(user['id'])
    assert user['id'] not in [u['id'] for u in api.users.list()]

def test_users_details_id_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.details('nope')

@pytest.mark.vcr()
def test_users_details_notfounderror(api):
    '''
    test to raise exception when user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.users.details(0)

@pytest.mark.vcr()
def test_users_details(api, user):
    '''
    test to get user details
    '''
    resp = api.users.details(user['id'])
    assert isinstance(user, dict)
    check(resp, 'id', int)
    check(resp, 'username', str)
    check(resp, 'name', str)
    check(resp, 'email', str)
    check(resp, 'permissions', int)
    check(resp, 'type', str)
    check(resp, 'login_fail_count', int)
    check(resp, 'login_fail_total', int)
    check(resp, 'enabled', bool)
    check(resp, 'uuid_id', 'uuid')

@pytest.mark.vcr()
def test_users_edit_id_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit('nope')

@pytest.mark.vcr()
def test_users_edit_permissions_typeerror(api):
    '''
    test to raise exception when type of permissions param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit(1, permissions='nope')

@pytest.mark.vcr()
def test_users_edit_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit(1, name=1)

@pytest.mark.vcr()
def test_users_edit_email_typeerror(api):
    '''
    test to raise exception when type of email param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit(1, email=1)

@pytest.mark.vcr()
def test_users_edit_enabled_typeerror(api):
    '''
    test to raise exception when type of enabled param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit(1, enabled='nope')

@pytest.mark.vcr()
def test_users_edit_notfounderror(api):
    '''
    test to raise exception when user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.users.edit(0, email=guser())

@pytest.mark.vcr()
def test_users_edit_permissionerror(stdapi, user):
    '''
    test to raise exception when standard user try to edit user.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.edit(user['id'], name=str(uuid.uuid4()))

@pytest.mark.vcr()
def test_users_edit(api, user):
    '''
    test to edit user
    '''
    resp = api.users.edit(user['id'], name='MODDED NAME')
    assert isinstance(user, dict)
    check(resp, 'id', int)
    check(resp, 'username', str)
    check(resp, 'name', str)
    check(resp, 'email', str)
    check(resp, 'permissions', int)
    check(resp, 'type', str)
    check(resp, 'login_fail_count', int)
    check(resp, 'login_fail_total', int)
    check(resp, 'enabled', bool)
    check(resp, 'uuid_id', 'uuid')
    assert resp['name'] == 'MODDED NAME'

@pytest.mark.vcr()
def test_users_enabled_id_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.enabled('nope', False)

@pytest.mark.vcr()
def test_users_enabled_enabled_typeerror(api):
    '''
    test to raise exception when type of enabled param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.enabled(1, 'nope')

@pytest.mark.vcr()
def test_users_enabled_notfounderror(api):
    '''
    test to raise exception when user provided user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.users.enabled(0, False)

@pytest.mark.vcr()
def test_users_enabled_permissionerror(stdapi, user):
    '''
    test to raise exception when standard user try to disable user.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.enabled(user['id'], False)

@pytest.mark.vcr()
def test_users_enabled(api, user):
    '''
    test to disable user
    '''
    disabled = api.users.enabled(user['id'], False)
    assert isinstance(disabled, dict)
    assert disabled['enabled'] is False

@pytest.mark.vcr()
def test_users_two_factor_id_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.two_factor('nope', False, False)

@pytest.mark.vcr()
def test_users_two_factor_email_typeerror(api):
    '''
    test to raise exception when type of email param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.two_factor(0, False, 'nope')

@pytest.mark.vcr()
def test_users_two_factor_sms_typeerror(api):
    '''
    test to raise exception when type of sms param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.two_factor('nope', False)

@pytest.mark.vcr()
def test_users_two_factor_phone_typeerror(api):
    '''
    test to raise exception when type of phone param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.two_factor(False, False, 8675309)

@pytest.mark.vcr()
@pytest.mark.xfail(raises=InvalidInputError)
def test_users_two_factor(api, user):
    '''
    test to configure two-factor authorization for a specific user
    '''
    api.users.two_factor(user['id'], False, False)

@pytest.mark.vcr()
def test_users_enable_two_factor_phone_typeerror(api):
    '''
    test to raise exception when type of phone param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.enable_two_factor(False)

@pytest.mark.vcr()
@pytest.mark.skip(reason="Don't want to enable two-facor on the user.")
def test_users_enable_two_factor(api):
    '''
    test to enable two_factor authentication for user.
    '''
    api.users.enable_two_factor('867-5309')

@pytest.mark.vcr()
def test_users_verify_two_factor_code_typeerror(api):
    '''
    test to raise exception when type of code param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.verify_two_factor(False)

@pytest.mark.vcr()
@pytest.mark.skip(reason="Don't want to enable two-factor on the user.")
def test_users_verify_two_factor(api):
    '''
    test to verify two_factor authentication for user.
    '''
    api.users.verify_two_factor(False)

@pytest.mark.vcr()
def test_users_impersonate_id_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.impersonate(1)
        api.session.restore()

@pytest.mark.vcr()
def test_users_impersonate_notfounderror(api):
    '''
    test to raise exception when user provided user_id not found.
    '''
    with pytest.raises(PermissionError):
        api.users.impersonate(guser())
        api.session.details()
        api.session.restore()

@pytest.mark.vcr()
def test_users_impersonate_permissionerror(stdapi, user):
    '''
    test to raise exception when standard user try to impersonate user.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.impersonate(user['username'])
        stdapi.session.details()
        stdapi.session.restore()

@pytest.mark.vcr()
def test_users_impersonate(api, user):
    '''
    test to impersonate user
    '''
    api.users.impersonate(user['username'])
    assert api.session.details()['username'] == user['username']
    api.session.restore()
    assert api.session.details()['username'] != user['username']

@pytest.mark.vcr()
def test_users_list_users(api, user):
    '''
    test to list users
    '''
    users = api.users.list()
    assert isinstance(users, list)
    assert user['id'] in [u['id']for u in users]

@pytest.mark.vcr()
def test_users_change_password_orig_typeerror(api):
    '''
    test to raise exception when type of old_password param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.change_password(0, False, 'nope')

@pytest.mark.vcr()
def test_users_change_password_new_typeerror(api):
    '''
    test to raise exception when type of new_password param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.change_password(0, 'nope', False)

@pytest.mark.vcr()
def test_users_change_password_id_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.change_password('fail', 'nope', 'nope')

@pytest.mark.vcr()
def test_users_change_password_notfounderror(api):
    '''
    test to raise exception when user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.users.change_password(0, 'nope', 'nope')

@pytest.mark.vcr()
def test_users_change_password_permissionserror(stdapi, user):
    '''
    test to raise exception when standard user try to change password.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.change_password(user['id'], 'nope', 'nope')

@pytest.mark.vcr()
def test_users_change_password(api):
    '''
    test to change password
    '''
    password = gpass()
    user = api.users.create(guser(), password, 16)
    api.users.change_password(user['id'], password, gpass())
    api.users.delete(user['id'])

@pytest.mark.vcr()
def test_users_list_auths_success(api, user):
    '''
    test to list user auths
    '''
    user_auth = api.users.list_auths(user['id'])
    assert isinstance(user, dict)
    check(user_auth, 'account_uuid', 'uuid')
    check(user_auth, 'api_permitted', bool)
    check(user_auth, 'password_permitted', bool)
    check(user_auth, 'saml_permitted', bool)
    check(user_auth, 'user_uuid', 'uuid')

@pytest.mark.vcr()
def test_users_list_auths_notfounderror(api):
    '''
    test to raise exception when user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.users.list_auths(1)

@pytest.mark.vcr()
def test_users_list_auths_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.list_auths('nope')

@pytest.mark.vcr()
def test_users_list_auths_permissionerror(stdapi, user):
    '''
    test to raise exception when standard user try to get list of user auths.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.list_auths(user['id'])

@pytest.mark.vcr()
def test_users_edit_auths_success(api, user):
    '''
    test to edit user auths
    '''
    api.users.edit_auths(user['id'], False, False, False)
    user_auth = api.users.list_auths(user['id'])
    assert user_auth['api_permitted'] is False
    assert user_auth['password_permitted'] is False
    assert user_auth['saml_permitted'] is False

@pytest.mark.vcr()
def test_users_edit_auths_notfounderror(api):
    '''
    test to raise exception when user_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.users.edit_auths(1)

@pytest.mark.vcr()
def test_users_edit_auths_typeerror(api):
    '''
    test to raise exception when type of user_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit_auths('nope')

@pytest.mark.vcr()
def test_users_edit_auths_api_permitted_typeerror(api, user):
    '''
    test to raise exception when type of api_permitted param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit_auths(user['id'], api_permitted='nope')

@pytest.mark.vcr()
def test_users_edit_auths_password_permitted_typeerror(api, user):
    '''
    test to raise exception when type of password_permitted param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit_auths(user['id'], password_permitted='nope')

@pytest.mark.vcr()
def test_users_edit_auths_saml_permitted_typeerror(api, user):
    '''
    test to raise exception when type of saml_permitted param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.users.edit_auths(user['id'], saml_permitted='nope')

@pytest.mark.vcr()
def test_users_edit_auths_permissionerror(stdapi, user):
    '''
    test to raise exception when standard user try to edit user auths.
    '''
    with pytest.raises(PermissionError):
        stdapi.users.edit_auths(user['id'])
