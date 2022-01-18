'''
Test Accounts API
'''
import requests
import responses

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

MSSP_ACCOUNTS_URL = 'https://cloud.tenable.com/api/v3/mssp/accounts'

accounts_us_east = [{
    'id': '2fd20a81-5dbf-4749-9173-62ba398c0641',
    'container_name': 'MSSP Example 1',
    'lms_customer_id': ' ',
    'custom_name': ' ',
    'sso_username': ' ',
    'region': 'US EAST',
    'site_id': 'test',
    'licensed_assets': 20,
    'licensed_assets_limit': 1000,
    'licensed_apps': [
        'was',
        'app'
    ],
    'notes': ' '
}
]


@responses.activate
def test_search(api):
    '''
    Test mssp accounts search method
    '''
    response = {
        'accounts': accounts_us_east,
        'pagination': {
            'total': len(accounts_us_east)
        }
    }

    fields = ['id', 'container_name', 'region', 'licensed_assets',
              'licensed_assets_limit', 'licensed_apps', 'notes', 'logo_uuid']

    filters = {'operator': 'eq', 'property': 'region', 'value': 'US EAST'}

    sort = [('container_name', 'asc')]

    api_payload = {
        'fields': fields,
        'filter': filters,
        'limit': 2,
        'sort': [{'property': 'container_name', 'order': 'asc'}],
    }

    responses.add(
        responses.POST,
        f'{MSSP_ACCOUNTS_URL}/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )

    resp = api.v3.mssp.accounts.search(fields=fields,
                                       filter=filters,
                                       sort=sort,
                                       limit=2)
    assert isinstance(resp, SearchIterator)

    for account in resp:
        assert account == response['accounts'][0]

    resp = api.v3.mssp.accounts.search(fields=fields,
                                       filter=filters,
                                       sort=sort,
                                       limit=2,
                                       return_csv=True
                                       )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.mssp.accounts.search(fields=fields,
                                       filter=filters,
                                       sort=sort,
                                       limit=2,
                                       return_resp=True
                                       )
    assert isinstance(resp, requests.Response)
