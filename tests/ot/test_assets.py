import pytest, responses

@responses.activate
def test_list(ot):
    '''
    Tests the list iterator
    '''
    responses.add(
        method='POST',
        url='https://localhost:443/v1/assets',
        json=[
            {
                'id': '000b3456-35f6-4b83-8ffe-45aceb288ce4',
                'name': 'Endpoint #548',
                'firstSeen': '2020-05-22T15:36:48.323534Z',
                'lastSeen': '2020-07-14T13:42:48.855494Z',
                'addresses': ['192.168.106.254'],
                'directAddresses': ['192.168.106.254'],
                'type': 'UnknownType',
                'purdueLevel': 'UnknownLevel',
                'vendor': 'Cisco',
                'runStatus': 'Unknown',
                'runStatusTime': '0001-01-01T00:00:00Z',
                'risk': 15.651708757702835,
                'criticality': 'LowCriticality',
                'hidden': False,
                'site': 'e4f7997b-8470-483c-a4b2-8fddcae22df3'
            }
        ]
    )
    resp = ot.assets.list()
    item = resp.next()
    assert item.id == '000b3456-35f6-4b83-8ffe-45aceb288ce4'
    assert item.name == 'Endpoint #548'
    assert item.firstSeen == '2020-05-22T15:36:48.323534Z'
    assert item.lastSeen == '2020-07-14T13:42:48.855494Z'
    assert item.addresses == ['192.168.106.254']
    assert item.directAddresses == ['192.168.106.254']
    assert item.type == 'UnknownType'
    assert item.purdueLevel == 'UnknownLevel'


@responses.activate
def test_details(ot):
    '''
    Tests the details method
    '''
    responses.add(
        method='GET',
        url='https://localhost:443/v1/assets/026fd8a1-2d50-4b2b-9cd5-285489d7fda4',
        json={
            'addresses': ['192.168.101.154'],
            'criticality': 'LowCriticality',
            'directAddresses': ['192.168.101.154'],
            'firstSeen': '2020-07-09T00:01:22.635465Z',
            'hidden': False,
            'id': '026fd8a1-2d50-4b2b-9cd5-285489d7fda4',
            'incidents': ['DirectConnectorIncident'],
            'lastSeen': '2020-07-09T00:10:51.125735Z',
            'name': 'Endpoint #608',
            'purdueLevel': 'UnknownLevel',
            'risk': 44.050849231996736,
            'runStatus': 'Unknown',
            'runStatusTime': '0001-01-01T00:00:00Z',
            'site': 'e4f7997b-8470-483c-a4b2-8fddcae22df3',
            'type': 'UnknownType'
        }
    )
    resp = ot.assets.details('026fd8a1-2d50-4b2b-9cd5-285489d7fda4')
    assert resp.id == '026fd8a1-2d50-4b2b-9cd5-285489d7fda4'
    assert resp.name == 'Endpoint #608'
    assert resp.lastSeen == '2020-07-09T00:10:51.125735Z'
    assert resp.addresses == ['192.168.101.154']
    assert resp.directAddresses == ['192.168.101.154']
    assert resp.type == 'UnknownType'
    assert resp.purdueLevel == 'UnknownLevel'


@responses.activate
def test_connections(ot):
    '''
    Tests the connections method
    '''
    responses.add(
        method='GET',
        url='https://localhost:443/v1/assets/026fd8a1-2d50-4b2b-9cd5-285489d7fda4/connections',
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
    resp = ot.assets.connections('026fd8a1-2d50-4b2b-9cd5-285489d7fda4')
    for item in resp:
        assert item.asset == '026fd8a1-2d50-4b2b-9cd5-285489d7fda4'
        assert item.networkInterface == 'd7f06b04-5733-44ac-9e84-096f6fdb181b'
        assert item.local == True
        assert item.direct == True
        assert item.connector.parts[0].connectionType == 'Direct'