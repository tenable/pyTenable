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
