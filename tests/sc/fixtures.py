import pytest, os, uuid
from tenable.sc import SecurityCenter
from tenable.errors import *
from tests.checker import check

@pytest.fixture(autouse=True, scope='module')
def sc(request):
    sc = SecurityCenter(os.environ['SC_TEST_HOST'], 
        port=int(os.environ['SC_TEST_PORT']))
    sc.login(os.environ['SC_TEST_USER'], os.environ['SC_TEST_PASS'])
    def teardown():
        sc.logout()
    request.addfinalizer(teardown)
    return sc