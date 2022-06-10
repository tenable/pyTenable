'''
Testing the search iterators for V3 endpoints
'''
import pytest

from tenable.io.v3.base.iterators.explore_iterator import SearchIterator

ASSET_DATA = [
    {'ipv6_addresses': [], 'netbios_name': 'DC1', 'sources': ['NESSUS_SCAN'],
     'last_licensed_scan_time': '2022-05-25T12:20:45.000Z', 'ipv4_addresses': ['172.26.48.10'],
     'aes': {'score': 755, 'is_predicted': True, 'confidence': 50.0},
     'network': {'id': '00000000-0000-0000-0000-000000000000', 'name': 'Default'},
     'display_ipv4_address': '172.26.48.10', 'first_observed': '2022-05-25T12:20:45.000Z',
     'acr': {'score': 6, 'calculated_score': 6, 'drivers': [{'values': ['general_server'], 'name': 'device_type'},
                                                            {'values': ['dns_server', 'directory_server'],
                                                             'name': 'device_capability'},
                                                            {'values': ['internal'], 'name': 'internet_exposure'}]},
     'is_deleted': False, 'last_observed': '2022-05-25T12:20:45.000Z', 'id': '88542bdc-7a3e-4b01-8ee3-87c09726eec5',
     'types': ['host'], 'created': '2022-05-25T12:20:47.346Z', 'observation_sources': [
        {'first_observed': '2022-05-25T12:20:45.000Z', 'last_observed': '2022-05-25T12:20:45.000Z',
         'name': 'NESSUS_SCAN'}], 'is_licensed': True, 'fqdns': ['dc1.target.tenablesecurity.com'], 'tags': [
        {'id': 'd74355e4-be1e-461b-ad7d-b842df740330', 'category': 'Target Groups', 'value': 'ATL PROD',
         'type': 'dynamic'},
        {'id': 'dc01ec2a-4872-4f09-8388-4538f43aa186', 'category': 'Test1', 'value': '11', 'type': 'dynamic'}],
     'operating_systems': ['Microsoft Windows Server 2008 R2 Datacenter Service Pack 1'],
     'display_fqdn': 'dc1.target.tenablesecurity.com',
     'display_operating_system': 'Microsoft Windows Server 2008 R2 Datacenter Service Pack 1',
     'system_type': 'general-purpose', 'installed_software': ['cpe:/a:microsoft:iis:7.5'], 'is_public': False,
     'name': 'dc1', 'updated': '2022-06-09T19:38:32.869Z', 'host_name': 'dc1'}
]


@pytest.mark.vcr()
def test_search_iterator_v3(api):
    '''
    Test for search iterator
    '''
    search_iterator = SearchIterator(
        api=api,
        _resource='assets',
        _path='api/v3/assets/search',
        _payload={
            "filter": {
                'and': [
                    {
                        "property": "name",
                        "operator": "eq",
                        "value": ["dc1"]
                    },
                    {
                        "property": "types",
                        "operator": "eq",
                        "value": ["host", "webapp", "cloud_resource"]
                    }
                ]
            }
        }
    )

    assert ASSET_DATA.__contains__(next(search_iterator))

    with pytest.raises(StopIteration):
        next(search_iterator)
