'''
Testing the search endpoint
'''
import responses
from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import SearchIterator

SEARCH_BASE_URL = r'https://cloud.tenable.com/api/v3/assets/search'

REQUESTDATA = dict(
    fields=['test1', 'test2'],
    filter=('netbios_name', 'eq', 'SCCM'),
    limit=10,
    sort=[('name', 'asc')],
)

REQUESTDATA_2 = dict(
    fields=['test1', 'test2'],
    filter=(
        'or',
        ('and', ('test', 'oper', '1'), ('test', 'oper', '2')),
        'and',
        ('test', 'oper', 3),
    ),
    limit=10,
    sort=[('name', 'asc'), {'property': 'bios_name', 'order': 'desc'}],
)

RESPONSE_2 = {
    'assets': [
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
            'tenable_id': '981465f994c546be8d19ed7522d3269d',
            'sources': ['NESSUS_AGENT'],
            'created': '2021-12-09T11:48:37.525Z',
            'observation_sources': [
                {
                    'first_observed': '2021-12-09T11:48:37.116Z',
                    'last_observed': '2021-12-09T11:48:37.116Z',
                    'name': 'NESSUS_AGENT',
                }
            ],
            'is_licensed': False,
            'ipv4_addresses': ['215.168.176.25'],
            'network': {
                'id': '00000000-0000-0000-0000-000000000000',
                'name': 'Default',
            },
            'display_ipv4_address': '215.168.176.25',
            'first_observed': '2021-12-09T11:48:37.116Z',
            'is_deleted': False,
            'last_observed': '2021-12-09T11:48:37.116Z',
            'is_public': True,
            'name': 'fncplqraaihnogjyyvkivljshdmigtbblsdlk',
            'id': '028e544c-8e39-42fa-abe0-c843dc41d93f',
            'updated': '2021-12-09T11:48:37.525Z',
            'host_name': 'fncplqraaihnogjyyvkivljshdmigtbblsdlk',
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
    ],
    'pagination': {
        'next':
            'H4sIAAAAAAAAADWOwQrCMBBE/2WO0kBrqtj+SillTTa4UE1JclBK/t2t4GlgZt/'
            'M7giyFk4Yd7xiOWRLceNUPhjhJdN9Zb9QQYPDphL1FvyWXDJqbZBjUmzaIV4Dyg'
            '51VpcpucdC4dc9obX+PHhm44O7mv4SOjMMxCZ0tu3I2T7cWii3ylO0zjb/N4T'
            'zwZ90Xwfm+gXgzWmZsQAAAA',
        'limit': 3,
        'total': 123,
    },
}


def test_search(api):
    search_iterator = ExploreBaseEndpoint(api).search(
        resource='assets', api_path='api/v3/assets/search', **REQUESTDATA
    )
    assert isinstance(search_iterator, SearchIterator)


@responses.activate
def test_search_response(api):
    responses.add(
        responses.POST, url=f'{SEARCH_BASE_URL}', json=RESPONSE_2, status=200
    )
    response = ExploreBaseEndpoint(api).search(
        resource='assets',
        api_path='api/v3/assets/search',
        is_sort_with_prop=False,
        return_resp=True,
        **REQUESTDATA_2,
    )
    assert isinstance(response, Response)
    assert RESPONSE_2 == response.json()


def test_parse_filter():
    '''
    Test case for parse filter method
    '''
    # Sampel filter value
    f_input: list = [
        ('name 1', 'operator 1', ['value 1', 'value 2']),
        ('name 1', 'operator 2', 'value 3,value 4')
    ]

    # filter response if rtype is sjson
    sjson_filter_response: dict = {
        'filter.0.filter': 'name 1',
        'filter.0.quality': 'operator 1',
        'filter.0.value': 'value 1,value 2',
        'filter.1.filter': 'name 1',
        'filter.1.quality': 'operator 2',
        'filter.1.value': 'value 3,value 4'
    }

    # filter response if rtype is json
    json_filter_response: dict = {
        'filters': [
            {
                'filter': 'name 1',
                'quality': 'operator 1',
                'value': 'value 1,value 2'
            },
            {
                'filter': 'name 1',
                'quality': 'operator 2',
                'value': 'value 3,value 4'
            }
        ]
    }

    # filter response if rtype is colon
    colon_filter_response: dict = {
        'f': [
            'name 1:operator 1:value 1,value 2',
            'name 1:operator 2:value 3,value 4'
        ]
    }

    # filter response if rtype is accessgroup
    accessgroup_filter_response: dict = {
        'rules': [
            {
                'operator': 'operator 1',
                'terms': [
                    'value 1',
                    'value 2'
                ],
                'type': 'name 1'
            },
            {
                'operator': 'operator 2',
                'terms': [
                    'value 3',
                    'value 4'
                ],
                'type': 'name 1'
            }
        ]
    }

    # filter response if rtype is assets
    assets_filter_response: dict = {
        'asset': [
            {
                'field': 'name 1',
                'operator': 'operator 1',
                'value': 'value 1,value 2'
            },
            {
                'field': 'name 1',
                'operator': 'operator 2',
                'value': 'value 3,value 4'
            }
        ]
    }

    # sample filter to validate data
    filter_set: dict = {
        'name 1': {
            'operators': [
                'operator 1',
                'operator 2'
            ],
            'choices': None,
            'pattern': '.*'
        }
    }

    sjson_filter_result = ExploreBaseEndpoint._parse_filters(
        finput=f_input,
        filterset=filter_set,
        rtype='sjson'
    )
    json_filter_result = ExploreBaseEndpoint._parse_filters(
        finput=f_input,
        filterset=filter_set,
        rtype='json'
    )
    colon_filter_result = ExploreBaseEndpoint._parse_filters(
        finput=f_input,
        filterset=filter_set,
        rtype='colon'
    )
    accessgroup_filter_result = ExploreBaseEndpoint._parse_filters(
        finput=f_input,
        filterset=filter_set,
        rtype='accessgroup'
    )
    assets_filter_result = ExploreBaseEndpoint._parse_filters(
        finput=f_input,
        filterset=filter_set,
        rtype='assets'
    )

    assert sjson_filter_result == sjson_filter_response
    assert json_filter_result == json_filter_response
    assert colon_filter_result == colon_filter_response
    assert accessgroup_filter_result == accessgroup_filter_response
    assert assets_filter_result == assets_filter_response
