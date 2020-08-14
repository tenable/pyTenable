from tenable.ot import TenableOT
from tenable.ot.assets import AssetsAPI
from tenable.ot.network_interfaces import NetworkInterfacesAPI
from tenable.ot.vulns import VulnsAPI
import pytest, responses

def test_ot_interfaces():
    '''
    Testing that the right interfaces are returned.
    '''
    ot = TenableOT()
    assert isinstance(ot.assets, AssetsAPI)
    assert isinstance(ot.network_interfaces, NetworkInterfacesAPI)
    assert isinstance(ot.vulns, VulnsAPI)


@responses.activate
def test_graph_api():
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
    ot = TenableOT(address='localhost')
    resp = ot.graphql(
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
    assert resp.data.asset.location == None