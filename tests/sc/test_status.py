from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_status_status(admin):
    s = admin.status.status()
    assert isinstance(s, dict)
    check(s, 'jobd', str)
    check(s, 'licenseStatus', str)
    check(s, 'PluginSubscriptionStatus', str, allow_none=True)
    check(s, 'LCEPluginSubscriptionStatus', str, allow_none=True)
    check(s, 'PassivePluginSubscriptionStatus', str, allow_none=True)
    check(s, 'pluginUpdates', dict)
    for key in s['pluginUpdates']:
        check(s['pluginUpdates'][key], 'updateTime', str)
        check(s['pluginUpdates'][key], 'stale', str)
    check(s, 'feedUpdates', dict)
    check(s['feedUpdates'], 'updateTime', str)
    check(s['feedUpdates'], 'stale', str)
    check(s, 'activeIPs', str)
    check(s, 'licensedIPs', str)