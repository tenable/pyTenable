from tenable.errors import *
from .fixtures import *
import uuid

def test_session_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.session.edit(1, 'nope')

def test_session_edit_email_typeerror(api):
    with pytest.raises(TypeError):
        api.session.edit('nope', 1)

def test_session_edit(api):
    api.session.edit(str(uuid.uuid4()), 'noreply@pytenable.test')

def test_session_get(api):
    assert isinstance(api.session.get(), dict)

def test_session_change_password_old_password_typeerror(api):
    with pytest.raises(TypeError):
        api.session.change_password(False, 'nope')

def test_session_change_password_new_password_typeerror(api):
    with pytest.raises(TypeError):
        api.session.change_password('nope', False)

@pytest.mark.skip(reason="Don't have old password")
def test_session_change_password(api):
    pass

@pytest.mark.skip(reason="Don't want to change the API keys")
def test_session_gen_api_keys(api):
    pass

def test_two_factor_email_typeerror(api):
    with pytest.raises(TypeError):
        api.session.two_factor(False, 'nope')

def test_two_factor_sms_typeerror(api):
    with pytest.raises(TypeError):
        api.session.two_factor('nope', False)

def test_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.session.two_factor(False, False, 8675309)

@pytest.mark.skip(reason="Don't want to enable two-facor on this user.")
def test_two_factor(api):
    api.session.two_factor(False, False)

def test_enable_two_factor_phone_typeerror(api):
    with pytest.raises(TypeError):
        api.session.enable_two_factor(False)

@pytest.mark.skip(reason="Don't want to enable two-facor on this user.")
def test_enable_two_factor(api):
    api.session.enable_two_factor('867-5309')

def test_verify_two_factor_code_typeerror(api):
    with pytest.raises(TypeError):
        api.session.verify_two_factor(False)

@pytest.mark.skip(reason="Don't want to enable two-facor on this user.")
def test_verify_two_factor(api):
    api.session.verify_two_factor(False)

@pytest.mark.skip(reason="We're testing this in the users test suite.")
# This is likely because we never impersonated in the first place.
def test_restore(api, user):
    pass