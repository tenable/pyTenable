'''
test base
'''
import responses

from tenable.ot.assets import AssetsAPI
from tenable.ot.network_interfaces import NetworkInterfacesAPI
from tenable.ot.vulns import VulnsAPI


def test_ot_interfaces(fixture_ot):
    '''
    Testing that the right interfaces are returned.
    '''
    assert isinstance(fixture_ot.assets, AssetsAPI)
    assert isinstance(fixture_ot.network_interfaces, NetworkInterfacesAPI)
    assert isinstance(fixture_ot.vulns, VulnsAPI)


@responses.activate
def test_graph_api(fixture_ot):
    '''
    Test the graph api method.
    '''
    responses.add(
        method='POST',
        url='https://localhost:443/graphql',
        json={
            'data': {
                'asset': {
                    'id': 'something',
                    'type': 'EngType',
                    'name': 'Eng. Station #40',
                    'criticality': 'HighCriticality',
                    'location': None
                }
            }
        }
    )
    resp = fixture_ot.graphql(
        variables={'asset': 'something'},
        query='''
            query getAssetDetails($asset: ID!) {
                asset(id: $asset) {
                    id
                    type
                    name
                    criticality
                    location
                }
            }
        '''
    )
    assert resp.data.asset.id == 'something'
    assert resp.data.asset.type == 'EngType'
    assert resp.data.asset.name == 'Eng. Station #40'
    assert resp.data.asset.criticality == 'HighCriticality'
    assert resp.data.asset.location is None
