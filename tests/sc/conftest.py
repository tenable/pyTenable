import pytest, os, uuid
from tenable.sc import TenableSC
from tenable.errors import *

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
    with vcr.use_cassette('sc_login', 
        filter_post_data_parameters=['username', 'password']):
        sc = TenableSC(os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'))
        sc.login(
            os.getenv('SC_TEST_USER', 'username'),
            os.getenv('SC_TEST_PASS', 'password'))
    def teardown():
        with vcr.use_cassette('sc_logout'):
            sc.logout()
    request.addfinalizer(teardown)
    return sc

@pytest.fixture(autouse=True, scope='module')
def admin(request, vcr):
    with vcr.use_cassette('sc_admin_login', 
        filter_post_data_parameters=['username', 'password']):
        sc = TenableSC(os.getenv('SC_TEST_HOST', 'securitycenter.home.cugnet.net'))
        sc.login(
            os.getenv('SC_TEST_ADMIN_USER', 'admin'),
            os.getenv('SC_TEST_ADMIN_PASS', 'password'))
    def teardown():
        with vcr.use_cassette('sc_logout'):
            sc.logout()
    request.addfinalizer(teardown)
    return sc