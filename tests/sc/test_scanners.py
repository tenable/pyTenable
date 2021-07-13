import pytest
from ..checker import check
from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception


@pytest.fixture
def scanner(request, admin, vcr):
    with vcr.use_cassette('test_scanners_create_success'):
        scanner = admin.scanners.create('Example', '127.0.0.1',
                                        username='nouser',
                                        password='nopassword')

    def teardown():
        try:
            with vcr.use_cassette('test_scanners_delete_success'):
                admin.scanners.delete(int(scanner['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return scanner


def test_scanners_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(name=1)


def test_scanners_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(description=1)


def test_scanners_constructor_username_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(username=1)


def test_scanners_constructor_cert_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(cert=1)


def test_scanners_constructor_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(password=1)


def test_scanners_constructor_address_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(address=1)


def test_scanners_constructor_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(port='one')


def test_scanners_constructor_proxy_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(proxy='one')


def test_scanners_constructor_verify_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(verify='yup')


def test_scanners_constructor_enabled_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(enabled='nope')


def test_scanners_constructor_managed_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(managed='yup')


def test_scanners_constructor_agent_capable_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(agent_capable='nope')


def test_scanners_constructor_zone_ids_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(zone_ids=1)


def test_scanners_constructor_zone_ids_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(zone_ids=['one'])


def test_scanners_constructor_orgs_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(orgs=1)


def test_scanners_constructor_orgs_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scanners._constructor(orgs=['one'])


def test_scanners_constructor_success(sc):
    resp = sc.scanners._constructor(
        name='Example',
        description='Described',
        username='username',
        password='password',
        address='scanner.company.tld',
        port=443,
        proxy=False,
        verify=False,
        enabled=True,
        managed=False,
        agent_capable=False,
        zone_ids=[1, 2, 3],
        orgs=[1, 2, 3]
    )
    assert resp == {
        'name': 'Example',
        'description': 'Described',
        'authType': 'password',
        'username': 'username',
        'password': 'password',
        'ip': 'scanner.company.tld',
        'port': 443,
        'useProxy': 'false',
        'verifyHost': 'false',
        'enabled': 'true',
        'managedPlugins': 'false',
        'agentCapable': 'false',
        'zones': [{'id': 1}, {'id': 2}, {'id': 3}],
        'nessusManagerOrgs': [{'id': 1}, {'id': 2}, {'id': 3}]
    }


@pytest.mark.vcr()
def test_scanners_create_success(scanner):
    assert isinstance(scanner, dict)
    check(scanner, 'id', str)
    check(scanner, 'name', str)
    check(scanner, 'description', str)
    check(scanner, 'ip', str)
    check(scanner, 'port', str)
    check(scanner, 'useProxy', str)
    check(scanner, 'enabled', str)
    check(scanner, 'verifyHost', str)
    check(scanner, 'managePlugins', str)
    check(scanner, 'authType', str)
    check(scanner, 'cert', str, allow_none=True)
    check(scanner, 'username', str, allow_none=True)
    check(scanner, 'password', str, allow_none=True)
    check(scanner, 'version', str, allow_none=True)
    check(scanner, 'webVersion', str, allow_none=True)
    check(scanner, 'admin', str)
    check(scanner, 'msp', str)
    check(scanner, 'numScans', str)
    check(scanner, 'numHosts', str)
    check(scanner, 'numSessions', str)
    check(scanner, 'numTCPSessions', str)
    check(scanner, 'loadAvg', str)
    check(scanner, 'uptime', int)
    check(scanner, 'status', str)
    check(scanner, 'pluginSet', str, allow_none=True)
    check(scanner, 'loadedPluginSet', str, allow_none=True)
    check(scanner, 'serverUUID', str, allow_none=True)
    check(scanner, 'createdTime', str)
    check(scanner, 'modifiedTime', str)
    check(scanner, 'zones', list)
    for zone in scanner['zones']:
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)
    check(scanner, 'nessusManagerOrgs', list)
    for org in scanner['nessusManagerOrgs']:
        check(org, 'id', str)
        check(org, 'name', str)
        check(org, 'description', str)


@pytest.mark.vcr()
def test_scanners_details_success(admin, scanner):
    scanner = admin.scanners.details(int(scanner['id']))
    assert isinstance(scanner, dict)
    check(scanner, 'id', str)
    check(scanner, 'name', str)
    check(scanner, 'description', str)
    check(scanner, 'ip', str)
    check(scanner, 'port', str)
    check(scanner, 'useProxy', str)
    check(scanner, 'enabled', str)
    check(scanner, 'verifyHost', str)
    check(scanner, 'managePlugins', str)
    check(scanner, 'authType', str)
    check(scanner, 'cert', str, allow_none=True)
    check(scanner, 'username', str, allow_none=True)
    check(scanner, 'password', str, allow_none=True)
    check(scanner, 'version', str, allow_none=True)
    check(scanner, 'webVersion', str, allow_none=True)
    check(scanner, 'admin', str)
    check(scanner, 'msp', str)
    check(scanner, 'numScans', str)
    check(scanner, 'numHosts', str)
    check(scanner, 'numSessions', str)
    check(scanner, 'numTCPSessions', str)
    check(scanner, 'loadAvg', str)
    check(scanner, 'uptime', int)
    check(scanner, 'status', str)
    check(scanner, 'pluginSet', str, allow_none=True)
    check(scanner, 'loadedPluginSet', str, allow_none=True)
    check(scanner, 'serverUUID', str, allow_none=True)
    check(scanner, 'createdTime', str)
    check(scanner, 'modifiedTime', str)
    check(scanner, 'zones', list)
    for zone in scanner['zones']:
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)
    check(scanner, 'nessusManagerOrgs', list)
    for org in scanner['nessusManagerOrgs']:
        check(org, 'id', str)
        check(org, 'name', str)
        check(org, 'description', str)


@pytest.mark.vcr()
def test_scanners_details_success_for_fields(admin, scanner):
    scanner = admin.scanners.details(int(scanner['id']), fields=['id', 'name', 'description'])
    assert isinstance(scanner, dict)
    check(scanner, 'id', str)
    check(scanner, 'name', str)
    check(scanner, 'description', str)


@pytest.mark.vcr()
def test_scanners_edit_success(admin, scanner):
    scanner = admin.scanners.edit(int(scanner['id']), name='Updated Scanner Name')
    assert isinstance(scanner, dict)
    check(scanner, 'id', str)
    check(scanner, 'name', str)
    assert scanner['name'] == 'Updated Scanner Name'
    check(scanner, 'description', str)
    check(scanner, 'ip', str)
    check(scanner, 'port', str)
    check(scanner, 'useProxy', str)
    check(scanner, 'enabled', str)
    check(scanner, 'verifyHost', str)
    check(scanner, 'managePlugins', str)
    check(scanner, 'authType', str)
    check(scanner, 'cert', str, allow_none=True)
    check(scanner, 'username', str, allow_none=True)
    check(scanner, 'password', str, allow_none=True)
    check(scanner, 'version', str, allow_none=True)
    check(scanner, 'webVersion', str, allow_none=True)
    check(scanner, 'admin', str)
    check(scanner, 'msp', str)
    check(scanner, 'numScans', str)
    check(scanner, 'numHosts', str)
    check(scanner, 'numSessions', str)
    check(scanner, 'numTCPSessions', str)
    check(scanner, 'loadAvg', str)
    check(scanner, 'uptime', int)
    check(scanner, 'status', str)
    check(scanner, 'pluginSet', str, allow_none=True)
    check(scanner, 'loadedPluginSet', str, allow_none=True)
    check(scanner, 'serverUUID', str, allow_none=True)
    check(scanner, 'createdTime', str)
    check(scanner, 'modifiedTime', str)
    check(scanner, 'zones', list)
    for zone in scanner['zones']:
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)
    check(scanner, 'nessusManagerOrgs', list)
    for org in scanner['nessusManagerOrgs']:
        check(org, 'id', str)
        check(org, 'name', str)
        check(org, 'description', str)


@pytest.mark.vcr()
def test_scanners_delete_success(admin, scanner):
    admin.scanners.delete(int(scanner['id']))


@pytest.mark.vcr()
def test_scanners_list_success(admin):
    for scanner in admin.scanners.list():
        check(scanner, 'id', str)
        check(scanner, 'name', str)
        check(scanner, 'description', str)
        check(scanner, 'status', str)


@pytest.mark.vcr()
def test_scanners_list_success_for_fields(admin, scanner):
    for s in admin.scanners.list(fields=['id', 'name', 'status', 'description']):
        check(s, 'id', str)
        check(s, 'name', str)
        check(s, 'status', str)
        check(s, 'description', str)


@pytest.mark.vcr()
@pytest.mark.skip(reason='No Agent Scanner in test env')
def test_scanners_agent_scans_success(admin, scanner):
    resp = admin.scanners.agent_scans(int(scanner['id']), '*')
    assert isinstance(resp, list)
    for scanner in resp:
        check(scanner, 'name', str)
        check(scanner, 'numResults', int)


@pytest.mark.vcr()
def test_scanners_update_status(admin, scanner):
    resp = admin.scanners.update_status()
    assert isinstance(resp, list)
    for scanner in resp:
        check(scanner, 'id', str)
        check(scanner, 'name', str)
        check(scanner, 'description', str)
        check(scanner, 'status', str)
