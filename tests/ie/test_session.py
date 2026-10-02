'''
test session
'''
import pytest
from tenable.ie import TenableIE
from tenable.errors import AuthenticationWarning


def test_session_authentication_error():
    '''
    test to raise the exception unauthorized session is created
    '''
    with pytest.warns(AuthenticationWarning):
        TenableIE(url='http://nourl')


def test_api_fixture_is_authenticated(api):
    '''
    The shared fixture must authenticate so tests exercise the real header.
    '''
    assert api._auth_mech == 'keys'
    assert 'X-API-Key' in api._session.headers
