'''
test server
'''
import pytest
from tests.checker import check

@pytest.mark.vcr()
def test_server_properties(api):
    '''
    test to get server properties
    '''
    resp = api.server.properties()
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

@pytest.mark.vcr()
def test_server_status(api):
    '''
    test to get server status
    '''
    status = api.server.status()
    assert isinstance(status, dict)
    check(status, 'code', int)
    check(status, 'status', str)
