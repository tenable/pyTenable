import responses
from ..checker import check


@responses.activate
def test_status_status(tsc):
    responses.get(
        'https://nourl/rest/status',
        json={
            'type': 'regular',
            'response': {
                'jobd': 'Running',
                'licenseStatus': 'Valid',
                'PluginSubscriptionStatus': 'Valid',
                'LCEPluginSubscriptionStatus': 'Expired',
                'PassivePluginSubscriptionStatus': None,
                'pluginUpdates': {
                    'active': {
                        'updateTime': '1553156153',
                        'stale': 'false',
                        'pluginCurrentSet': '201903202042',
                    },
                    'passive': {'updateTime': '1553148005', 'stale': 'false'},
                    'lce': {'updateTime': '1550205301', 'stale': 'true'},
                },
                'feedUpdates': {'updateTime': '1553145023', 'stale': 'false'},
                'activeIPs': '46',
                'licensedIPs': '102400',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553202508,
        },
    )
    s = tsc.status.status()
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
