from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_server_properties(api):
    p = api.server.properties()
    assert isinstance(p, dict)
    check(p, 'analytics', dict)
    check(p['analytics'], 'enabled', bool)
    check(p['analytics'], 'key', str)
    check(p['analytics'], 'site_id', str)
    check(p, 'capabilities', dict)
    check(p, 'expiration', int)
    check(p, 'expiration_time', int)
    check(p, 'idle_timeout', str)
    check(p, 'license', dict)
    check(p['license'], 'agents', int)
    check(p['license'], 'agents_used', int)
    check(p['license'], 'apps', dict) 
    check(p['license'], 'evaluation', bool)
    check(p['license'], 'expiration_date', int)
    check(p['license'], 'ips', int)
    check(p['license'], 'scanners', int)
    check(p['license'], 'scanners_used', int)
    check(p['license'], 'users', int)
    check(p, 'loaded_plugin_set', str)
    check(p, 'login_banner', str, allow_none=True)
    check(p, 'notifications', list)

@pytest.mark.vcr()
def test_server_status(api):
    s = api.server.status()
    assert isinstance(s, dict)
    check(s, 'code', int)
    check(s, 'status', str)