import os

import pytest
from requests.models import Response

from tenable.errors import ConnectionError, APIError
from tenable.sc import TenableSC


def test_init_connection_error():
    with pytest.raises(ConnectionError):
        TenableSC(os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
                  vendor='pytest',
                  product='pytenable-automated-testing', cert='cert', adapter='adapter')


def test_init_self_details_connection_error(vcr):
    with vcr.use_cassette('sc_login_error',
                          filter_post_data_parameters=['username', 'password']):
        with pytest.raises(ConnectionError):
            TenableSC(os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
                      vendor='pytest',
                      product='pytenable-automated-testing')


def test_enter(sc):
    assert sc == sc.__enter__()


def test_exit(sc, vcr):
    with vcr.use_cassette('sc_login'):
        sc.__exit__(exc_type='exc_type', exc_value='exc_value', exc_traceback='exc_traceback')



def test_resp_error_check(sc, vcr):
    with pytest.raises(AttributeError):
        response = Response()
        response._content = b'{ "error_code": 401}'
        sc._resp_error_check(response)
    # pass
    response = Response()
    response._content = b'{ "error_code": 401, }'
    sc._resp_error_check(response)


def test_log_in(sc):
    with pytest.raises(ConnectionError):
        sc.login(access_key='access_key', secret_key='secret_key')
    sc.version = '5.14.0'
    sc.login(access_key='access_key', secret_key='secret_key')
    assert sc._apikeys
