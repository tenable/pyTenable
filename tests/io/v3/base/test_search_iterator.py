'''
Testing the CSV iterators
'''

import responses

from tenable.io.v3.base.iterators.explore_iterator import SearchIterator

USERS_BASE_URL = r'https://cloud.tenable.com/api/v3/assets/search'

ASSET_DATA = [
    {
        'ipv6_addresses': [],
        'types': ['host'],
        'sources': ['test_v3'],
        'created': '2021-11-24T13:43:56.709Z',
        'observation_sources': [
            {
                'first_observed': '2021-11-24T13:43:56.442Z',
                'last_observed': '2021-11-24T13:43:56.442Z',
                'name': 'test_v3',
            }
        ],
        'is_licensed': False,
        'ipv4_addresses': ['192.12.13.7'],
        'network': {
            'id': '00000000-0000-0000-0000-000000000000',
            'name': 'Default',
        },
        'display_ipv4_address': '192.12.13.7',
        'first_observed': '2021-11-24T13:43:56.442Z',
        'is_deleted': False,
        'last_observed': '2021-11-24T13:43:56.442Z',
        'is_public': True,
        'name': '192.12.13.7',
        'id': '0142df77-dbc4-4706-8456-b756c06ee8a2',
        'updated': '2021-11-24T13:43:56.709Z',
    },
    {
        'ipv6_addresses': [],
        'types': ['host'],
        'sources': ['test_v3'],
        'created': '2021-11-24T13:46:11.566Z',
        'observation_sources': [
            {
                'first_observed': '2021-11-24T13:46:11.283Z',
                'last_observed': '2021-11-24T13:46:11.283Z',
                'name': 'test_v3',
            }
        ],
        'is_licensed': False,
        'ipv4_addresses': ['192.12.13.29'],
        'network': {
            'id': '00000000-0000-0000-0000-000000000000',
            'name': 'Default',
        },
        'display_ipv4_address': '192.12.13.29',
        'first_observed': '2021-11-24T13:46:11.283Z',
        'is_deleted': False,
        'last_observed': '2021-11-24T13:46:11.283Z',
        'is_public': True,
        'name': '192.12.13.29',
        'id': '03d29dee-dfc6-45f1-99ae-f1301ac34f80',
        'updated': '2021-11-24T13:46:11.566Z',
    },
    {
        'ipv6_addresses': [],
        'netbios_name': 'SCCM',
        'tenable_id': '5ad355cfa93d49da9ac9391c60b6a486',
        'sources': ['NESSUS_SCAN'],
        'last_licensed_scan_time': '2021-11-02T13:51:20.000Z',
        'ipv4_addresses': ['172.26.48.115'],
        'display_mac_address': '00:50:56:a6:55:63',
        'bios_id': '119d2642-47d2-906c-b08c-1c52b8be074b',
        'network': {
            'id': '00000000-0000-0000-0000-000000000000',
            'name': 'Default',
        },
        'display_ipv4_address': '172.26.48.115',
        'first_observed': '2021-11-02T13:51:20.000Z',
        'is_deleted': False,
        'last_observed': '2021-11-02T13:51:20.000Z',
        'last_authenticated_scan_time': '2021-11-02T13:51:20.000Z',
        'id': '06178fcf-90ba-476b-9ce3-a6fcf32fc88c',
        'mac_addresses': ['00:50:56:a6:55:63'],
        'types': ['host'],
        'created': '2021-11-02T13:51:30.967Z',
        'observation_sources': [
            {
                'first_observed': '2021-11-02T13:51:20.000Z',
                'last_observed': '2021-11-02T13:51:20.000Z',
                'name': 'NESSUS_SCAN',
            }
        ],
        'is_licensed': True,
        'fqdns': ['sccm.target.tenablesecurity.com'],
        'operating_systems': [
            'Microsoft Windows Server 2008 R2 Standard Service Pack 1'
        ],
        'display_fqdn': 'sccm.target.tenablesecurity.com',
        'display_operating_system':
            'Microsoft Windows Server 2008 R2 Standard Service Pack 1',
        'system_type': 'general-purpose',
        'is_public': False,
        'name': 'sccm',
        'updated': '2021-11-02T13:51:31.305Z',
        'host_name': 'sccm',
    },
]
PAGINATION = {'next': 'H4sIAAAAAAAAADWOSwrDMAxE7zL', 'limit': 3, 'total': 111}


@responses.activate
def test_search_iterator(api):
    responses.add(
        method=responses.POST,
        url=USERS_BASE_URL,
        json={'assets': ASSET_DATA, 'pagination': PAGINATION},
    )

    search_iterator = SearchIterator(
        api=api, _resource='assets', _path='api/v3/assets/search', _payload={}
    )

    assert ASSET_DATA.__contains__(next(search_iterator))
