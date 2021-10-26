'''
configuration which would be used for testing sc.
'''
import os

import pytest

from tenable.errors import APIError, NotFoundError
from tenable.sc import TenableSC
from tests.pytenable_log_handler import setup_logging_to_file, log_exception


@pytest.fixture(scope='module')
def vcr_config():
    '''
    test fixture for vcr_config
    '''
    return {
        'filter_headers': [
            ('Cookie', 'TNS_SESSIONID=SESSIONID'),
            ('X-SecurityCenter', '0000000000'),
        ],
    }


@pytest.fixture(autouse=True, scope='module')
def security_center(request, vcr):
    '''
    test fixture for sc(security center)
    '''
    setup_logging_to_file()
    with vcr.use_cassette('sc_login',
                          filter_post_data_parameters=['username',
                                                       'password'
                                                       ]):
        tenable_security_center = TenableSC(
            os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing')
        tenable_security_center.login(
            os.getenv('SC_TEST_USER', 'username'),
            os.getenv('SC_TEST_PASS', 'password'))
        tenable_security_center.version  # noqa: PLW0104

    def teardown():
        try:
            with vcr.use_cassette('sc_login'):
                tenable_security_center.logout()
        except NotFoundError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return tenable_security_center


@pytest.fixture(autouse=True, scope='module')
def admin(request, vcr):
    '''
    test fixture for admin
    '''
    with vcr.use_cassette('sc_login',
                          filter_post_data_parameters=['username',
                                                       'password'
                                                       ]):
        sc = TenableSC(  # noqa: PLC0103
            os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing')
        sc.login(
            os.getenv('SC_TEST_ADMIN_USER', 'admin'),
            os.getenv('SC_TEST_ADMIN_PASS', 'password'))
        sc.version  # noqa: PLW0104

    def teardown():
        with vcr.use_cassette('sc_login'):
            sc.logout()

    request.addfinalizer(teardown)
    return sc


@pytest.fixture(autouse=True, scope='module')
def unauth(vcr):
    '''
    test fixture for un_authorization
    '''
    with vcr.use_cassette('sc_login',
                          filter_post_data_parameters=['username',
                                                       'password'
                                                       ]):
        sc = TenableSC(  # noqa: PLC0103
            os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing')
    return sc


@pytest.fixture
def group(request, security_center, vcr):
    '''
    test fixture for un_authorization
    '''
    with vcr.use_cassette('test_groups_create_success'):
        grp = security_center.groups.create('groupname')

    def teardown():
        try:
            with vcr.use_cassette('test_groups_delete_success'):
                security_center.groups.delete(int(grp['id']))
        except APIError:
            pass

    request.addfinalizer(teardown)
    return grp
