'''
test __init__
'''
import pytest
from requests import Response
from tenable.io import TenableIO
from tenable.errors import UnexpectedValueError


def test_init_unexpected_value_error():
    '''

    test to raise the exception when no api keys are provided

    '''
    with pytest.raises(UnexpectedValueError):
        TenableIO()


def test_retry_request():
    '''

    test to raise the exception when requested to retry the connection

    '''
    with pytest.raises(UnexpectedValueError):
        response = Response()
        response._content = b'{"error_code": 404}'
        getattr(TenableIO()._retry_request, '_retry_request')({'response': response._content,
                                                               'retries': 3,
                                                               'kwargs': None})
