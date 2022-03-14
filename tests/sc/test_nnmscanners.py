'''
test file for testing various scenarios in securitycenter's nnm functionality
'''
import pytest

from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception
from ..checker import check


@pytest.fixture
def nnm(request, admin, vcr):
    '''
    test fixture for nnm
    '''
    with vcr.use_cassette('test_nnm_create_success'):
        nnm = admin.nnm.create('Example', '127.0.0.1',
                                        username='admin',
                                        password='password')

    def teardown():
        try:
            with vcr.use_cassette('test_nnm_delete_success'):
                admin.nnm.delete(int(nnm['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return nnm


def test_nnm_constructor_name_typeerror(security_center):
    '''
    test nnm for name type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(name=1)


def test_nnm_constructor_description_typeerror(security_center):
    '''
    test nnm constructor for description type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(description=1)


def test_nnm_constructor_username_typeerror(security_center):
    '''
    test nnm constructor for username type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(username=1)


def test_nnm_constructor_cert_typeerror(security_center):
    '''
    test nnm constructor for 'cert' type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(cert=1)


def test_nnm_constructor_password_typeerror(security_center):
    '''
    test nnm constructor for password type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(password=1)


def test_nnm_constructor_address_typeerror(security_center):
    '''
    test nnm constructor for address type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(address=1)


def test_nnm_constructor_port_typeerror(security_center):
    '''
    test nnm constructor for port type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(port='one')


def test_nnm_constructor_proxy_typeerror(security_center):
    '''
    test nnm constructor for proxy type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(proxy='one')


def test_nnm_constructor_verify_typeerror(security_center):
    '''
    test nnm constructor for verify type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(verify='yup')


def test_nnm_constructor_enabled_typeerror(security_center):
    '''
    test nnm constructor for enabled type error
    '''
    with pytest.raises(TypeError):
        security_center.nnm._constructor(enabled='nope')


def test_nnm_constructor_success(security_center):
    '''
    test nnm constructor for success
    '''
    resp = security_center.nnm._constructor(
        name='Example',
        description='Described',
        username='admin',
        password='password',
        address='127.0.0.1',
        port=8443,
        proxy=False,
        verify=False,
        enabled=True,
    )
    assert resp == {
        'name': 'Example',
        'description': 'Described',
        'authType': 'password',
        'username': 'admin',
        'password': 'password',
        'ip': '127.0.0.1',
        'port': 8443,
        'useProxy': 'false',
        'verifyHost': 'false',
        'enabled': 'true',
    }


@pytest.mark.vcr()
def test_nnm_create_success(nnm):
    '''
    test nnm create for success
    '''
    assert isinstance(nnm, dict)
    check(nnm, 'id', str)
    check(nnm, 'name', str)
    check(nnm, 'description', str)
    check(nnm, 'ip', str)
    check(nnm, 'port', str)
    check(nnm, 'useProxy', str)
    check(nnm, 'enabled', str)
    check(nnm, 'verifyHost', str)
    check(nnm, 'authType', str)
    check(nnm, 'cert', str, allow_none=True)
    check(nnm, 'username', str, allow_none=True)
    check(nnm, 'password', str, allow_none=True)
    check(nnm, 'version', str, allow_none=True)
    check(nnm, 'webVersion', str, allow_none=True)
    check(nnm, 'admin', str)
    check(nnm, 'uptime', int)
    check(nnm, 'status', str)
    check(nnm, 'pluginSet', str, allow_none=True)
    check(nnm, 'loadedPluginSet', str, allow_none=True)
    check(nnm, 'createdTime', str)
    check(nnm, 'modifiedTime', str)

@pytest.mark.vcr()
def test_nnm_details_success(admin, nnm):
    '''
    test nnm details for success
    '''
    nnm = admin.nnm.details(int(nnm['id']))
    assert isinstance(nnm, dict)
    check(nnm, 'id', str)
    check(nnm, 'name', str)
    check(nnm, 'description', str)
    check(nnm, 'ip', str)
    check(nnm, 'port', str)
    check(nnm, 'useProxy', str)
    check(nnm, 'enabled', str)
    check(nnm, 'verifyHost', str)
    check(nnm, 'authType', str)
    check(nnm, 'cert', str, allow_none=True)
    check(nnm, 'username', str, allow_none=True)
    check(nnm, 'password', str, allow_none=True)
    check(nnm, 'version', str, allow_none=True)
    check(nnm, 'webVersion', str, allow_none=True)
    check(nnm, 'admin', str)
    check(nnm, 'uptime', int)
    check(nnm, 'status', str)
    check(nnm, 'pluginSet', str, allow_none=True)
    check(nnm, 'loadedPluginSet', str, allow_none=True)
    check(nnm, 'createdTime', str)
    check(nnm, 'modifiedTime', str)

@pytest.mark.vcr()
def test_nnm_details_success_for_fields(admin, nnm):
    '''
    test nnm details success for fields
    '''
    nnm = admin.nnm.details(int(nnm['id']), fields=['id', 'name', 'description'])
    assert isinstance(nnm, dict)
    check(nnm, 'id', str)
    check(nnm, 'name', str)
    check(nnm, 'description', str)


@pytest.mark.vcr()
def test_nnm_edit_success(admin, nnm):
    '''
    test nnm edit for success
    '''
    nnm = admin.nnm.edit(int(nnm['id']), name='Updated nnm Name')
    assert isinstance(nnm, dict)
    check(nnm, 'id', str)
    check(nnm, 'name', str)
    assert nnm['name'] == 'Updated nnm Name'
    check(nnm, 'description', str)
    check(nnm, 'ip', str)
    check(nnm, 'port', str)
    check(nnm, 'useProxy', str)
    check(nnm, 'enabled', str)
    check(nnm, 'verifyHost', str)
    check(nnm, 'managePlugins', str)
    check(nnm, 'authType', str)
    check(nnm, 'cert', str, allow_none=True)
    check(nnm, 'username', str, allow_none=True)
    check(nnm, 'password', str, allow_none=True)
    check(nnm, 'version', str, allow_none=True)
    check(nnm, 'webVersion', str, allow_none=True)
    check(nnm, 'admin', str)
    check(nnm, 'uptime', int)
    check(nnm, 'status', str)
    check(nnm, 'pluginSet', str, allow_none=True)
    check(nnm, 'loadedPluginSet', str, allow_none=True)
    check(nnm, 'createdTime', str)
    check(nnm, 'modifiedTime', str)

@pytest.mark.vcr()
def test_nnm_delete_success(admin, nnm):
    '''
    test nnm delete for success
    '''
    admin.nnm.delete(int(nnm['id']))


@pytest.mark.vcr()
def test_nnm_list_success(admin):
    '''
    test nnm list for success
    '''
    for nnm in admin.nnm.list():
        check(nnm, 'id', str)
        check(nnm, 'name', str)
        check(nnm, 'description', str)
        check(nnm, 'status', str)


@pytest.mark.vcr()
def test_nnm_list_success_for_fields(admin, nnm):
    '''
    test nnm list success for fields
    '''
    for nnm_scanner in admin.nnm.list(fields=['id', 'name', 'status', 'description']):
        check(nnm_scanner, 'id', str)
        check(nnm_scanner, 'name', str)
        check(nnm_scanner, 'status', str)
        check(nnm_scanner, 'description', str)



@pytest.mark.vcr()
def test_nnm_update_status(admin, nnm):
    '''
    test nnm update status for success
    '''
    resp = admin.nnm.update_status()
    assert isinstance(resp, list)
    for nnm in resp:
        check(nnm, 'id', str)
        check(nnm, 'name', str)
        check(nnm, 'description', str)
        check(nnm, 'status', str)
