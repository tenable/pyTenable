"""
test file for testing various scenarios in security center's scanners functionality
"""

import pytest
import responses
from responses import matchers

from ..checker import check


@pytest.fixture
def scanner():
    """
    test fixture for scanner
    """
    return {
        'id': '9',
        'name': 'Example',
        'description': '',
        'ip': '127.0.0.1',
        'port': '8834',
        'useProxy': 'false',
        'enabled': 'true',
        'verifyHost': 'false',
        'managePlugins': 'false',
        'authType': 'password',
        'cert': None,
        'username': 'nouser',
        'password': 'SET',
        'agentCapable': 'false',
        'version': None,
        'webVersion': None,
        'admin': 'false',
        'msp': 'false',
        'numScans': '0',
        'numHosts': '0',
        'numSessions': '0',
        'numTCPSessions': '0',
        'loadAvg': '0.0',
        'uptime': -1,
        'status': '8192',
        'pluginSet': None,
        'loadedPluginSet': None,
        'serverUUID': None,
        'createdTime': '1553266985',
        'modifiedTime': '1553266985',
        'zones': [],
        'nessusManagerOrgs': [],
    }


def test_scanners_constructor_name_typeerror(tsc):
    """
    test scanners constructor for name type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(name=1)


def test_scanners_constructor_description_typeerror(tsc):
    """
    test scanners constructor for description type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(description=1)


def test_scanners_constructor_username_typeerror(tsc):
    """
    test scanners constructor for username type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(username=1)


def test_scanners_constructor_cert_typeerror(tsc):
    """
    test scanners constructor for 'cert' type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(cert=1)


def test_scanners_constructor_password_typeerror(tsc):
    """
    test scanners constructor for password type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(password=1)


def test_scanners_constructor_address_typeerror(tsc):
    """
    test scanners constructor for address type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(address=1)


def test_scanners_constructor_port_typeerror(tsc):
    """
    test scanners constructor for port type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(port='one')


def test_scanners_constructor_proxy_typeerror(tsc):
    """
    test scanners constructor for proxy type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(proxy='one')


def test_scanners_constructor_verify_typeerror(tsc):
    """
    test scanners constructor for verify type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(verify='yup')


def test_scanners_constructor_enabled_typeerror(tsc):
    """
    test scanners constructor for enabled type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(enabled='nope')


def test_scanners_constructor_managed_typeerror(tsc):
    """
    test scanners constructor for managed type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(managed='yup')


def test_scanners_constructor_agent_capable_typeerror(tsc):
    """
    test scanners constructor for 'agent capable' type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(agent_capable='nope')


def test_scanners_constructor_zone_ids_typeerror(tsc):
    """
    test scanners constructor for 'zone ids' type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(zone_ids=1)


def test_scanners_constructor_zone_ids_item_typeerror(tsc):
    """
    test scanners constructor for 'zone ids item' type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(zone_ids=['one'])


def test_scanners_constructor_orgs_typeerror(tsc):
    """
    test scanners constructor for orgs type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(orgs=1)


def test_scanners_constructor_orgs_item_typeerror(tsc):
    """
    test scanners constructor for 'orgs item' type error
    """
    with pytest.raises(TypeError):
        tsc.scanners._constructor(orgs=['one'])


def test_scanners_constructor_success(tsc):
    """
    test scanners constructor for success
    """
    resp = tsc.scanners._constructor(
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
        orgs=[1, 2, 3],
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
        'nessusManagerOrgs': [{'id': 1}, {'id': 2}, {'id': 3}],
    }


@responses.activate
def test_scanners_create_success(tsc):
    """
    test scanners create for success
    """
    responses.post(
        'https://nourl/rest/scanner',
        json={
            'type': 'regular',
            'response': {
                'id': '9',
                'name': 'Example',
                'description': '',
                'ip': '127.0.0.1',
                'port': '8834',
                'useProxy': 'false',
                'enabled': 'true',
                'verifyHost': 'false',
                'managePlugins': 'false',
                'authType': 'password',
                'cert': None,
                'username': 'nouser',
                'password': 'SET',
                'agentCapable': 'false',
                'version': None,
                'webVersion': None,
                'admin': 'false',
                'msp': 'false',
                'numScans': '0',
                'numHosts': '0',
                'numSessions': '0',
                'numTCPSessions': '0',
                'loadAvg': '0.0',
                'uptime': -1,
                'status': '8192',
                'pluginSet': None,
                'loadedPluginSet': None,
                'serverUUID': None,
                'createdTime': '1553266985',
                'modifiedTime': '1553266985',
                'zones': [],
                'nessusManagerOrgs': [],
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1553266985,
        },
    )
    scanner = tsc.scanners.create(
        'Example', '127.0.0.1', username='nouser', password='nopassword'
    )
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


@responses.activate
def test_scanners_details_success(tsc, scanner):
    """
    test scanners details for success
    """
    responses.get(
        'https://nourl/rest/scanner/9',
        json={
            'type': 'regular',
            'response': {
                'id': '10',
                'name': 'Example',
                'description': '',
                'ip': '127.0.0.1',
                'port': '8834',
                'useProxy': 'false',
                'enabled': 'true',
                'verifyHost': 'false',
                'managePlugins': 'false',
                'authType': 'password',
                'cert': None,
                'username': 'nouser',
                'password': 'SET',
                'agentCapable': 'false',
                'version': None,
                'webVersion': None,
                'admin': 'false',
                'msp': 'false',
                'numScans': '0',
                'numHosts': '0',
                'numSessions': '0',
                'numTCPSessions': '0',
                'loadAvg': '0.0',
                'uptime': -1,
                'status': '8192',
                'pluginSet': None,
                'loadedPluginSet': None,
                'serverUUID': None,
                'createdTime': '1553266985',
                'modifiedTime': '1553266985',
                'zones': [],
                'nessusManagerOrgs': [],
                'certInfo': '',
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1553266985,
        },
    )
    scanner = tsc.scanners.details(int(scanner['id']))
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


@responses.activate
def test_scanners_details_success_for_fields(tsc, scanner):
    """
    test scanners details success for fields
    """
    responses.get(
        'https://nourl/rest/scanner/9',
        json={
            'type': 'regular',
            'response': {'id': '10', 'name': 'Example', 'description': ''},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553266985,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    scanner = tsc.scanners.details(
        int(scanner['id']), fields=['id', 'name', 'description']
    )
    assert isinstance(scanner, dict)
    check(scanner, 'id', str)
    check(scanner, 'name', str)
    check(scanner, 'description', str)


@responses.activate
def test_scanners_edit_success(tsc, scanner):
    """
    test scanners edit for success
    """
    responses.patch(
        'https://nourl/rest/scanner/9',
        json={
            'type': 'regular',
            'response': {
                'id': '25',
                'name': 'Updated Scanner Name',
                'description': '',
                'ip': '127.0.0.1',
                'port': '8834',
                'useProxy': 'false',
                'enabled': 'true',
                'verifyHost': 'false',
                'managePlugins': 'false',
                'authType': 'password',
                'cert': None,
                'username': 'nouser',
                'password': 'SET',
                'agentCapable': 'false',
                'version': None,
                'webVersion': None,
                'admin': 'false',
                'msp': 'false',
                'numScans': '0',
                'numHosts': '0',
                'numSessions': '0',
                'numTCPSessions': '0',
                'loadAvg': '0.0',
                'uptime': -1,
                'status': '8192',
                'pluginSet': None,
                'loadedPluginSet': None,
                'serverUUID': None,
                'createdTime': '1553267776',
                'modifiedTime': '1553267777',
                'zones': [],
                'nessusManagerOrgs': [],
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1553267776,
        },
    )
    scanner = tsc.scanners.edit(int(scanner['id']), name='Updated Scanner Name')
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


@responses.activate
def test_scanners_delete_success(tsc, scanner):
    """
    test scanners delete for success
    """
    responses.delete(
        'https://nourl/rest/scanner/9',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553266987,
        },
    )
    tsc.scanners.delete(int(scanner['id']))


@responses.activate
def test_scanners_list_success(tsc):
    """
    test scanners list for success
    """
    responses.get(
        'https://nourl/rest/scanner',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '1',
                    'name': 'Internal Scanner',
                    'description': '',
                    'agentCapable': 'false',
                    'status': '1',
                },
                {
                    'id': '2',
                    'name': 'Tenable.io',
                    'description': '',
                    'agentCapable': 'true',
                    'status': '1',
                },
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553266988,
        },
    )
    for scanner in tsc.scanners.list():
        check(scanner, 'id', str)
        check(scanner, 'name', str)
        check(scanner, 'description', str)
        check(scanner, 'status', str)


@responses.activate
def test_scanners_list_success_for_fields(tsc, scanner):
    """
    test scanners list success for fields
    """
    responses.get(
        'https://nourl/rest/scanner',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '1',
                    'name': 'Internal Scanner',
                    'description': '',
                    'status': '1',
                },
                {'id': '2', 'name': 'Tenable.io', 'description': '', 'status': '1'},
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553266988,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,status,description'})],
    )
    for a_scanner in tsc.scanners.list(fields=['id', 'name', 'status', 'description']):
        check(a_scanner, 'id', str)
        check(a_scanner, 'name', str)
        check(a_scanner, 'status', str)
        check(a_scanner, 'description', str)


@pytest.mark.skip(reason='No Agent Scanner in test env')
def test_scanners_agent_scans_success(tsc, scanner):
    """
    test scanners agent scans for success
    """
    resp = tsc.scanners.agent_scans(int(scanner['id']), '*')
    assert isinstance(resp, list)
    for scanner in resp:
        check(scanner, 'name', str)
        check(scanner, 'numResults', int)


@responses.activate
def test_scanners_update_status(tsc, scanner):
    """
    test scanners update status for success
    """
    responses.post(
        'https://nourl/rest/scanner/updateStatus',
        json={
            'type': 'regular',
            'response': {
                'status': [
                    {
                        'id': '1',
                        'name': 'Internal Scanner',
                        'description': '',
                        'status': '8193',
                    },
                    {
                        'id': '2',
                        'name': 'Tenable.io',
                        'description': '',
                        'status': '8193',
                    },
                ]
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553266989,
        },
    )
    resp = tsc.scanners.update_status()
    assert isinstance(resp, list)
    for scanner in resp:
        check(scanner, 'id', str)
        check(scanner, 'name', str)
        check(scanner, 'description', str)
        check(scanner, 'status', str)
