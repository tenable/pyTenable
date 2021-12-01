'''
test session
'''
import pytest
from tenable.ad import TenableAD
from tenable.errors import AuthenticationWarning


def test_session_authentication_error():
    '''
    test to raise the exception unauthorized session is created
    '''
    with pytest.warns(AuthenticationWarning):
        TenableAD()._session_auth()
