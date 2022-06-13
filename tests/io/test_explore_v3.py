'''
Testing the search for V3 endpoints
'''
import pytest
from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import SearchIterator

REQUESTDATA = dict(
    fields=['name'],
    filter=(
        'and',
        ('last_observed', 'lt', '2022-06-08T18:30:00.000Z'),
    ),
    limit=2,
    sort=[('name', 'asc')],
)

REQUESTDATA_2 = dict(
    fields=['name'],
    filter=(
        'and',
        ('last_observed', 'lt', '2022-06-08T18:30:00.000Z'),
    ),
    limit=3,
    sort=[('name', 'asc')],
)

RESPONSE_2 = {'assets':
                  [{'created': '2022-01-24T22:28:15.083Z',
                    'display_ipv4_address': '172.26.100.153',
                    'display_mac_address': '00:50:56:a6:64:8d',
                    'display_operating_system': 'Windows Server 2016 Standard 14393',
                    'first_observed': '2022-01-24T22:27:58.000Z',
                    'host_name': '......server01',
                    'id': '557db40c-b546-4281-8976-5e29d32a6622',
                    'ipv4_addresses': ['172.26.100.153'],
                    'ipv6_addresses': [],
                    'is_deleted': False,
                    'is_licensed': False,
                    'is_public': False,
                    'last_licensed_scan_time': '2022-01-24T22:27:58.000Z',
                    'last_observed': '2022-01-24T22:27:58.000Z',
                    'mac_addresses': ['00:50:56:a6:64:8d'],
                    'name': '......server01',
                    'netbios_name': '......SERVER01',
                    'network': {'id': '00000000-0000-0000-0000-000000000000',
                                'name': 'Default'},
                    'observation_sources': [{'first_observed': '2022-01-24T22:27:58.000Z',
                                             'last_observed': '2022-01-24T22:27:58.000Z',
                                             'name': 'NESSUS_SCAN'}],
                    'operating_systems': ['Windows Server 2016 Standard 14393'],
                    'sources': ['NESSUS_SCAN'],
                    'system_type': 'general-purpose',
                    'tags': [{'category': 'ab',
                              'id': '0aeb8d1b-869d-4520-8f02-775201885780',
                              'type': 'dynamic',
                              'value': 'test_tag'},
                             {'category': 'CS-scan manger',
                              'id': 'f2dc798f-97e7-4295-bdad-d186dc28503a',
                              'type': 'dynamic',
                              'value': 'manager'}],
                    'types': ['host'],
                    'updated': '2022-06-09T02:59:22.736Z'},
                   {'created': '2021-10-21T18:58:31.027Z',
                    'display_ipv4_address': '0.10.203.164',
                    'display_mac_address': '00:00:00:29:0f:7c',
                    'first_observed': '2021-10-21T18:58:15.000Z',
                    'id': '82db057b-3327-476b-9b32-2cf6c751850d',
                    'installed_software': ['cpe:/a:openbsd:openssh:8.3'],
                    'ipv4_addresses': ['0.10.203.164'],
                    'ipv6_addresses': [],
                    'is_deleted': False,
                    'is_licensed': False,
                    'is_public': True,
                    'last_licensed_scan_time': '2021-10-21T18:58:15.000Z',
                    'last_observed': '2021-10-21T18:58:15.000Z',
                    'mac_addresses': ['00:00:00:29:0f:7c'],
                    'name': '0.10.203.164',
                    'network': {'id': '00000000-0000-0000-0000-000000000000',
                                'name': 'Default'},
                    'observation_sources': [{'first_observed': '2021-10-21T18:58:15.000Z',
                                             'last_observed': '2021-10-21T18:58:15.000Z',
                                             'name': 'NESSUS_SCAN'}],
                    'sources': ['NESSUS_SCAN'],
                    'tags': [{'category': 'ab',
                              'id': '0aeb8d1b-869d-4520-8f02-775201885780',
                              'type': 'dynamic',
                              'value': 'test_tag'}],
                    'types': ['host'],
                    'updated': '2022-01-19T13:39:02.995Z'},
                   {'created': '2021-10-21T17:38:53.966Z',
                    'display_ipv4_address': '0.10.204.254',
                    'first_observed': '2021-10-21T17:38:39.000Z',
                    'id': '37643fd5-74a9-4e7c-915a-c90a14e61dfb',
                    'ipv4_addresses': ['0.10.204.254'],
                    'ipv6_addresses': [],
                    'is_deleted': False,
                    'is_licensed': False,
                    'is_public': True,
                    'last_licensed_scan_time': '2021-10-21T17:38:39.000Z',
                    'last_observed': '2021-10-21T17:38:39.000Z',
                    'name': '0.10.204.254',
                    'network': {'id': '00000000-0000-0000-0000-000000000000',
                                'name': 'Default'},
                    'observation_sources': [{'first_observed': '2021-10-21T17:38:39.000Z',
                                             'last_observed': '2021-10-21T17:38:39.000Z',
                                             'name': 'NESSUS_SCAN'}],
                    'sources': ['NESSUS_SCAN'],
                    'tags': [{'category': 'ab',
                              'id': '0aeb8d1b-869d-4520-8f02-775201885780',
                              'type': 'dynamic',
                              'value': 'test_tag'}],
                    'types': ['host'],
                    'updated': '2022-01-19T13:25:12.796Z'}],
              'pagination': {'limit': 3,
                             'next': 'H4sIAAAAAAAAAH2Q0W6DMAxF/8WPE0EGAhS+o0+rEDLEqJEooUlaDSH+fYGpUreHPV7LPvfIKwx69GyhXoEmBfVlhdmama1foIb7g+0S+2VmBxHsY/ImLAPfQ37S+OAQrsZ52KJ/CCM535rOsX2y+k0a/RspxTQVWAg8nZNTnWGNGCPiJ2zNzp+M30Xf8Eo76kZWLfk/gl/aeQfbfgjOWH+I/dhMdNvLyPWHtVav0IRVJttfWxqOp1wA4wTjFGWc5jI0ZGUhs0HlopRUCcllL6okJ9FXSInkIlFDBwEz6psOlVn0ktXhgwH3ERihr9m+AaS0jLF5AQAA',
                             'total': 102931}}


@pytest.mark.vcr()
def test_search_v3(api):
    '''
    Test for search SearchIterator method iterator
    '''
    search_iterator = ExploreBaseEndpoint(api)._search(
        resource='assets',
        api_path='api/v3/assets/host/search',
        **REQUESTDATA
    )
    assert isinstance(search_iterator, SearchIterator)


@pytest.mark.vcr()
def test_search_response_v3(api):
    '''
    Test for search method response
    '''
    response = ExploreBaseEndpoint(api)._search(
        resource='assets',
        api_path='api/v3/assets/host/search',
        return_resp=True,
        **REQUESTDATA_2,
    )
    assert isinstance(response, Response)
    assert RESPONSE_2 == response.json()
