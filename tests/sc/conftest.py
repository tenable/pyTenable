import pytest, os, uuid
from tenable.sc import TenableSC
from tenable.errors import *

#@pytest.fixture(scope='module')
#def vcr_config():
#    return {
#        'filter_headers': [
#            ('X-APIKeys', 'accessKey=TIO_ACCESS_KEY;secretKey=TIO_SECRET_KEY'),
#            ('x-request-uuid', 'ffffffffffffffffffffffffffffffff'),
#        ],
#    }


@pytest.fixture(autouse=True, scope='module')
def sc(request, vcr):
    with vcr.use_cassette('sc_login', filter_post_data_parameters=['username', 'password']):
        sc = TenableSC(os.getenv('SC_TEST_HOST'), 
            port=int(os.getenv('SC_TEST_PORT')))
        sc.login(os.getenv('SC_TEST_USER'), os.getenv('SC_TEST_PASS'))
    def teardown():
        with vcr.use_cassette('sc_logout'):
            sc.logout()
    request.addfinalizer(teardown)
    return sc