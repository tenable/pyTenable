'''
test file to test various scenarios in init.py
'''
import os

import pytest
from requests.models import Response

from requests.exceptions import ConnectionError as RequestsConnectionError
from tenable.errors import ConnectionError
from tenable.sc import TenableSC


def test_init_connection_error():
    '''
    test init for connection error
    '''
    with pytest.raises(RequestsConnectionError):
        TenableSC(host='nothing_here',
                  username='something',
                  password='something',
                  vendor='pytest',
                  product='pytenable-automated-testing')


#def test_init_self_details_connection_error(vcr):
#    '''
#    test init self details for connection error
#    '''
#    with vcr.use_cassette('sc_login_error',
#                          filter_post_data_parameters=['username', 'password']):
#        with pytest.warn(AuthenticationWarning):
#            TenableSC(os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
#                      vendor='pytest',
#                      product='pytenable-automated-testing',
#            )


def test_enter(security_center):
    '''
    test enter
    '''
    assert security_center == security_center.__enter__()


def test_exit(security_center, vcr):
    '''
    test exit
    '''
    with vcr.use_cassette('sc_login'):
        security_center.__exit__(exc_type='exc_type', exc_value='exc_value', exc_traceback='exc_traceback')


def test_resp_error_check(security_center):
    '''
    test response error check
    '''
    with pytest.raises(AttributeError):
        response = Response()
        response._content = b'{ "error_code": 401}'
        security_center._resp_error_check(response)
    # pass
    response = Response()
    response._content = b'{ "error_code": 401, }'
    security_center._resp_error_check(response)


def test_log_in(vcr):
    '''
    test log in
    '''
    tsc = TenableSC(url='https://localhost')
    tsc._version = '5.12.0'
    with pytest.raises(ConnectionError):
        tsc.login(access_key='access_key', secret_key='secret_key')

    tsc._version = '5.14.0'
    tsc.login(access_key='access_key', secret_key='secret_key')
    assert tsc._auth_mech == 'keys'

    tsc._version = None
    tsc._auth_mech = None
    with vcr.use_cassette('sc_login_5_20_0'):
        tsc.login(access_key='access_key', secret_key='secret_key')
        assert tsc._auth_mech == 'keys'
