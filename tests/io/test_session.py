from ..checker import check, single
from tenable.errors import *
import uuid, pytest

@pytest.mark.vcr()
def test_session_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.session.edit(1, 'nope')

@pytest.mark.vcr()
def test_session_edit_email_typeerror(api):
    with pytest.raises(TypeError):
        api.session.edit('nope', 1)

@pytest.mark.vcr()
def test_session_edit(api):
    api.session.edit(str(uuid.uuid4()), 'noreply@pytenable.test')

@pytest.mark.vcr()
def test_session_details(api):
    session = api.session.details()
    assert isinstance(session, dict)
    check(session, 'container_id', int)
    check(session, 'container_uuid', 'uuid')
    check(session, 'container_name', str)
    check(session, 'email', str)
    check(session, 'enabled', bool)
    check(session, 'group_uuids', list)
    check(session, 'groups', list)
    check(session, 'id', int)
    check(session, 'login_fail_count', int)
    check(session, 'login_fail_total', int)
    check(session, 'name', str)
    check(session, 'user_name', str)
    check(session, 'username', str)
    check(session, 'uuid', 'uuid')
    check(session, 'uuid_id', str)
    check(session, 'features', dict)
    for item in session['features'].keys():
        check(session['features'], item, bool)

@pytest.mark.vcr()
def test_session_change_password_old_password_typeerror(api):
    with pytest.raises(TypeError):
        api.session.change_password(False, 'nope')

@pytest.mark.vcr()
def test_session_change_password_new_password_typeerror(api):
    with pytest.raises(TypeError):
        api.session.change_password('nope', False)

@pytest.mark.skip(reason="Don't have old password")
def test_session_change_password(api):
    pass

@pytest.mark.skip(reason="Don't want to change the API keys")
def test_session_gen_api_keys(api):
    pass

@pytest.mark.vcr()
def test_session_two_factor_email_typeerror(api):
    with pytest.raises(TypeError):
        api.session.two_factor(False, 'nope')

@pytest.mark.vcr()
def test_session_two_factor_sms_typeerror(api):
    with pytest.raises(TypeError):
        api.session.two_factor('nope', False)

@pytest.mark.vcr()
def test_session_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.session.two_factor(False, False, 8675309)

@pytest.mark.skip(reason="Don't want to enable two-facor on this user.")
def test_session_two_factor(api):
    api.session.two_factor(False, False)

@pytest.mark.vcr()
def test_session_enable_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.session.enable_two_factor(False)

@pytest.mark.skip(reason="Don't want to enable two-facor on this user.")
def test_session_enable_two_factor(api):
    api.session.enable_two_factor('867-5309')

@pytest.mark.vcr()
def test_session_verify_two_factor_code_typeerror(api):
    with pytest.raises(TypeError):
        api.session.verify_two_factor(False)

@pytest.mark.skip(reason="Don't want to enable two-facor on this user.")
def test_session_verify_two_factor(api):
    api.session.verify_two_factor(False)

@pytest.mark.skip(reason="We're testing this in the users test suite.")
# This is likely because we never impersonated in the first place.
def test_session_restore(api, user):
    pass