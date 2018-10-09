from .fixtures import *
from tenable.errors import *
import uuid

def guser():
    return '{}@pytenable.io'.format(uuid.uuid4())

def gpass():
    return '{}Tt!'.format(uuid.uuid4())

def test_create_username_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(False, gpass(), 1)

def test_create_password_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), False, 1)

def test_create_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 'nope')

def test_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, name=1)

def test_create_email_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, email=1)

def test_create_account_type_typeerror(api):
    with pytest.raises(TypeError):
        api.users.create(guser(), gpass(), 1, account_type=False)

def test_create_permissionserror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.users.create(guser(), gpass(), 16)

def test_create(api, user):
    pass

def test_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.delete('False')

def test_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.delete(0)

def test_delete_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.delete(user['id'])

def test_delete(api, user):
    api.users.delete(user['id'])
    assert user['id'] not in [u['id'] for u in api.users.list()]

def test_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.details('nope')

def test_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.details(0)

def test_details(api, user):
    dets = api.users.details(user['id'])
    assert isinstance(dets, dict)
    assert dets['id'] == user['id']

def test_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit('nope')

def test_edit_permissions_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, permissions='nope')

def test_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, name=1)

def test_edit_email_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, email=1)

def test_edit_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.users.edit(1, enabled='false')

def test_edit_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.edit(0, email=guser())

def test_edit_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.edit(user['id'], name=str(uuid.uuid4()))

def test_edit(api, user):
    name = guser()
    modded = api.users.edit(user['id'], name=name)
    assert modded['name'] == name

def test_enabled_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.enabled('nope', False)

def test_enabled_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.users.enabled(1, 'nope')

def test_enabled_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.enabled(0, False)

def test_enabled_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.enabled(user['id'], False)

def test_enabled(api, user):
    disabled = api.users.enabled(user['id'], False)
    assert isinstance(disabled, dict)
    assert disabled['enabled'] == False

def test_two_factor_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor('nope', False, False)

def test_two_factor_email_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor(0, False, 'nope')

def test_two_factor_sms_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor('nope', False)

def test_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.users.two_factor(False, False, 8675309)

@pytest.mark.xfail(raises=InvalidInputError)
def test_two_factor(api, user):
    api.users.two_factor(user['id'], False, False)

def test_enable_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.users.enable_two_factor(False)

@pytest.mark.skip(reason="Don't want to enable two-facor on the user.")
def test_enable_two_factor(api):
    api.users.enable_two_factor('867-5309')

def test_verify_two_factor_code_typeerror(api):
    with pytest.raises(TypeError):
        api.users.verify_two_factor(False)

@pytest.mark.skip(reason="Don't want to enable two-facor on the user.")
def test_verify_two_factor(api):
    api.users.verify_two_factor(False)

def test_impersonate_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.impersonate(1)
        api.session.restore()

def test_impersonate_notfounderror(api):
    with pytest.raises(PermissionError):
        api.users.impersonate(guser())
        api.session.get()
        api.session.restore()

def test_impersonate_permissionerror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.impersonate(user['username'])
        stdapi.session.get()
        stdapi.session.restore()

def test_impersonate(api, user):
    api.users.impersonate(user['username'])
    assert api.session.get()['username'] == user['username']
    api.session.restore()
    assert api.session.get()['username'] != user['username']

def test_list_users(api, user):
    users = api.users.list()
    assert isinstance(users, list)
    assert user['id'] in [u['id']for u in users]

def test_change_password_orig_typeerror(api):
    with pytest.raises(TypeError):
        api.users.change_password(0, False, 'nope')

def test_change_password_new_typeerror(api):
    with pytest.raises(TypeError):
        api.users.change_password(0, 'nope', False)

def test_change_password_id_typeerror(api):
    with pytest.raises(TypeError):
        api.users.change_password('fail', 'nope', 'nope')

def test_change_password_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.users.change_password(0, 'nope', 'nope')

def test_change_password_permissionserror(stdapi, user):
    with pytest.raises(PermissionError):
        stdapi.users.change_password(user['id'], 'nope', 'nope')

def test_change_password(api):
    password = gpass()
    user = api.users.create(guser(), password, 16)
    api.users.change_password(user['id'], password, gpass())
    api.users.delete(user['id'])