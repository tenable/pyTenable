"""
configuration which would be used for testing sc.
"""

import os

import pytest
import responses

from tenable.errors import APIError, NotFoundError
from tenable.sc import TenableSC
from tests.pytenable_log_handler import log_exception, setup_logging_to_file


@pytest.fixture(scope='module')
def vcr_config():
    """
    test fixture for vcr_config
    """
    return {
        'filter_headers': [
            ('Cookie', 'TNS_SESSIONID=SESSIONID'),
            ('X-SecurityCenter', '0000000000'),
        ],
    }


@pytest.fixture(autouse=True, scope='module')
@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def security_center(request, vcr):
    """
    test fixture for sc(security center)
    """
    setup_logging_to_file()
    with vcr.use_cassette(
        'sc_login', filter_post_data_parameters=['username', 'password']
    ):
        tenable_security_center = TenableSC(
            url=os.getenv('SC_TEST_URL', 'https://securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing',
            username='username',
            password='password',
        )

    def teardown():
        try:
            with vcr.use_cassette('sc_login'):
                tenable_security_center.logout()
        except NotFoundError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return tenable_security_center


@pytest.fixture(autouse=True, scope='module')
@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def admin(request, vcr):
    """
    test fixture for admin
    """
    with vcr.use_cassette(
        'sc_login', filter_post_data_parameters=['username', 'password']
    ):
        sc = TenableSC(  # noqa: PLC0103
            url=os.getenv('SC_TEST_URL', 'https://securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing',
            username='admin',
            password='password',
        )

    def teardown():
        with vcr.use_cassette('sc_login'):
            sc.logout()

    request.addfinalizer(teardown)
    return sc


@pytest.fixture(autouse=True, scope='module')
@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def unauth(vcr):
    """
    test fixture for un_authorization
    """
    with vcr.use_cassette(
        'sc_login', filter_post_data_parameters=['username', 'password']
    ):
        sc = TenableSC(  # noqa: PLC0103
            url=os.getenv('SC_TEST_URL', 'https://securitycenter.home.cugnet.net'),
            vendor='pytest',
            product='pytenable-automated-testing',
        )
    return sc


@pytest.fixture
def group(request, security_center, vcr):
    """
    test fixture for un_authorization
    """
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


@pytest.fixture
def tsc():
    with responses.RequestsMock() as rsps:
        rsps.get(
            'https://nourl/rest/system',
            json={'error_code': None, 'response': {'version': '6.4.0'}},
        )
        return TenableSC(
            url='https://nourl', access_key='SOMETHING', secret_key='SECRET'
        )
