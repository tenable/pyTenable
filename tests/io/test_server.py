"""
test server
"""

import responses
from tests.checker import check


@responses.activate
def test_server_properties(tvm):
    """
    test to get server properties
    """
    responses.add(
        responses.GET,
        'https://nourl/server/properties',
        json={
            'limitEnabled': False,
            'loaded_plugin_set': '201812051251',
            'server_uuid': '417457f6-cd2b-727c-d94f-06bce34d74cf27789b39c292efc6',
            'update': {'href': None, 'new_version': 0, 'restart': 0},
            'expiration': 1893304800,
            'nessus_ui_version': '11.0.46',
            'nessus_type': 'Nessus Cloud',
            'notifications': [],
            'expiration_time': 4041,
            'license': {
                'expiration_date': 1893304800,
                'ips': -1,
                'agents': -1,
                'users': -1,
                'scanners': -1,
                'evaluation': False,
                'scanners_used': 0,
                'agents_used': 0,
                'apps': {},
            },
            'enterprise': True,
            'analytics': {
                'key': 'ddf4b2ef-ac5e-4ee7-701d-7fd1a95bc458',
                'enabled': True,
                'site_id': 'us-2b',
            },
            'msp': True,
            'server_build': 'C20023',
            'force_ui_reload': True,
            'capabilities': {
                'multi_user': 'full',
                'multi_scanner': True,
                'report_email_config': True,
                'two_factor': {'twilio': True, 'smtp': False},
            },
            'plugin_set': '201812051251',
            'idle_timeout': '30',
            'nessus_ui_build': '155',
            'scanner_boottime': 1531265862,
            'evaluation': {'limitEnabled': True, 'targets': 25},
            'container_db_version': '10.43.0',
            'login_banner': None,
            'server_version': '6.9.1',
        },
    )
    resp = tvm.server.properties()
    assert isinstance(resp, dict)
    check(resp, 'analytics', dict)
    check(resp['analytics'], 'enabled', bool)
    check(resp['analytics'], 'key', str)
    check(resp['analytics'], 'site_id', str)
    if 'capabilities' in resp:
        check(resp, 'capabilities', dict)
        check(resp['capabilities'], 'multi_scanner', bool)
        check(resp['capabilities'], 'multi_user', str)
        check(resp['capabilities'], 'report_email_config', bool)
        check(resp['capabilities'], 'two_factor', dict)
        check(resp['capabilities']['two_factor'], 'smtp', bool)
        check(resp['capabilities']['two_factor'], 'twilio', bool)
    check(resp, 'evaluation', dict)
    check(resp['evaluation'], 'limitEnabled', bool)
    check(resp['evaluation'], 'targets', int)
    if 'expiration' in resp:
        check(resp, 'expiration', int)
    if 'expiration_time' in resp:
        check(resp, 'expiration_time', int)
    check(resp, 'force_ui_reload', bool)
    if 'idle_timeout' in resp:
        check(resp, 'idle_timeout', str)
    if 'license' in resp:
        check(resp, 'license', dict)
        check(resp['license'], 'agents', int)
        check(resp['license'], 'apps', dict)
        check(resp['license'], 'evaluation', bool)
        check(resp['license'], 'expiration_date', int)
        check(resp['license'], 'ips', int)
        check(resp['license'], 'scanners', int)
        check(resp['license'], 'users', int)
    if 'loaded_plugin_set' in resp:
        check(resp, 'loaded_plugin_set', str)
    if 'login_banner' in resp:
        check(resp, 'login_banner', str, allow_none=True)
    if 'msp' in resp:
        check(resp, 'msp', bool)
    check(resp, 'nessus_type', str)
    check(resp, 'nessus_ui_build', str)
    check(resp, 'nessus_ui_version', str)
    if 'notifications' in resp:
        check(resp, 'notifications', list)
    if 'plugin_set' in resp:
        check(resp, 'plugin_set', str)
    if 'update' in resp:
        check(resp, 'update', dict)


@responses.activate
def test_server_status(tvm):
    """
    test to get server status
    """
    responses.add(
        responses.GET,
        'https://nourl/server/status',
        json={'code': 200, 'status': 'ready'},
    )
    status = tvm.server.status()
    assert isinstance(status, dict)
    check(status, 'code', int)
    check(status, 'status', str)
