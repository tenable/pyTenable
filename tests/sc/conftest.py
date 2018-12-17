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

@pytest.mark.vcr(filter_post_data_parameters=['username', 'password'])
@pytest.fixture(autouse=True, scope='module')
def sc(request):
    sc = TenableSC(os.getenv('SC_TEST_HOST'), 
        port=int(os.getenv('SC_TEST_PORT')))
    sc.login(os.getenv('SC_TEST_USER'), os.getenv('SC_TEST_PASS'))
    def teardown():
        sc.logout()
    request.addfinalizer(teardown)
    return sc