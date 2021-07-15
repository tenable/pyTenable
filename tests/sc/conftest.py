import os
import pytest
from tenable.sc import TenableSC
from tests.pytenable_log_handler import setup_logging_to_file, log_exception
from tenable.errors import APIError, NotFoundError


@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_headers': [
            ('Cookie', 'TNS_SESSIONID=SESSIONID'),
            ('X-SecurityCenter', '0000000000'),
        ],
    }


@pytest.fixture(autouse=True, scope='module')
def sc(request, vcr):
    setup_logging_to_file()
    with vcr.use_cassette('sc_login',
                          filter_post_data_parameters=['username', 'password']):
        sc = TenableSC(
            os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing')
        sc.login(
            os.getenv('SC_TEST_USER', 'username'),
            os.getenv('SC_TEST_PASS', 'password'))

    def teardown():
        try:
            with vcr.use_cassette('sc_login'):
                sc.logout()
        except NotFoundError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return sc


@pytest.fixture(autouse=True, scope='module')
def admin(request, vcr):
    with vcr.use_cassette('sc_login',
                          filter_post_data_parameters=['username', 'password']):
        sc = TenableSC(
            os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing')
        sc.login(
            os.getenv('SC_TEST_ADMIN_USER', 'admin'),
            os.getenv('SC_TEST_ADMIN_PASS', 'password'))

    def teardown():
        with vcr.use_cassette('sc_login'):
            sc.logout()

    request.addfinalizer(teardown)
    return sc


@pytest.fixture(autouse=True, scope='module')
def unauth(request, vcr):
    with vcr.use_cassette('sc_login',
                          filter_post_data_parameters=['username', 'password']):
        sc = TenableSC(
            os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing')
    return sc


@pytest.fixture
def group(request, sc, vcr):
    with vcr.use_cassette('test_groups_create_success'):
        group = sc.groups.create('groupname')

    def teardown():
        try:
            with vcr.use_cassette('test_groups_delete_success'):
                sc.groups.delete(int(group['id']))
        except APIError:
            pass

    request.addfinalizer(teardown)
    return group
