import pytest, responses


@responses.activate
def test_details(ot):
    '''
    Tests the details method
    '''
    responses.add(
        method='GET',
        url='https://localhost:443/v1/networkinterfaces/d7f06b04-5733-44ac-9e84-096f6fdb181b',
        json={
            'id': 'd7f06b04-5733-44ac-9e84-096f6fdb181b',
            'ips': ['192.168.101.154'],
            'dnsNames': None,
            'lastSeen': '2020-07-09T00:10:51.125735Z',
            'firstSeen': '2020-07-09T00:01:22.618953Z',
            'family': 'Unknown'
        }
    )
    resp = ot.network_interfaces.details('d7f06b04-5733-44ac-9e84-096f6fdb181b')
    assert resp.id == 'd7f06b04-5733-44ac-9e84-096f6fdb181b'
    assert resp.ips == ['192.168.101.154']
    assert resp.dnsNames == None
    assert resp.lastSeen == '2020-07-09T00:10:51.125735Z'
    assert resp.firstSeen == '2020-07-09T00:01:22.618953Z'
    assert resp.family == 'Unknown'


@responses.activate
def test_connections(ot):
    '''
    Test the connections method
    '''
    responses.add(
        method='GET',
        url='https://localhost:443/v1/networkinterfaces/d7f06b04-5733-44ac-9e84-096f6fdb181b/connections',
        json=[{
            'asset': '026fd8a1-2d50-4b2b-9cd5-285489d7fda4',
            'networkInterface': 'd7f06b04-5733-44ac-9e84-096f6fdb181b',
            'local': True,
            'direct': True,
            'connector': {
                'parts': [
                    {'connectionType': 'Direct'}
                ]
            }
        }]
    )
    resp = ot.network_interfaces.connections('d7f06b04-5733-44ac-9e84-096f6fdb181b')
    for item in resp:
        assert item.asset == '026fd8a1-2d50-4b2b-9cd5-285489d7fda4'
        assert item.networkInterface == 'd7f06b04-5733-44ac-9e84-096f6fdb181b'
        assert item.local == True
        assert item.direct == True
        assert item.connector.parts[0].connectionType == 'Direct'