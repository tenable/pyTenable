'''
test __init__
'''
import pytest
from requests import Response
from tenable.io import TenableIO
from tenable.errors import UnexpectedValueError, AuthenticationWarning


def test_init_unexpected_value_error():
    '''

    test to raise the exception when no api keys are provided

    '''
    with pytest.warns(AuthenticationWarning):
        TenableIO()


#def test_retry_request():
#    '''
#
#    test to raise the exception when requested to retry the connection
#
#    '''
#    with pytest.raises(UnexpectedValueError):
#        response = Response()
#        response._content = b'{"error_code": 404}'
#        getattr(TenableIO(), '_retry_request')(response=response,
#                                               retries=3,
#                                               kwargs={}
#                                               )
