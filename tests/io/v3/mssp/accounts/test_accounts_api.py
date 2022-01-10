import responses

MSSP_ACCOUNTS_URL = 'https://cloud.tenable.com/api/v3/mssp/accounts'

accounts_us_east = [
    {
        'id': '2fd20a81-5dbf-4749-9173-62ba398c0641',
        'container_name': 'MSSP Example 1',
        'region': 'US East',
        'licensed_assets': 0,
        'licensed_assets_limit': 1024,
        'licensed_apps': [],
        'logo_uuid': '46cf08ec-8d67-4232-848e-b229faa86e7a'
    },
    {
        'id': '10a3ad73-6220-4197-97e8-c7acb2a4d19a',
        'container_name': 'MSSP Example 3',
        'region': 'US East',
        'licensed_assets': 0,
        'licensed_assets_limit': -1,
        'licensed_apps': [],
        'notes': 'Notes test',
        'logo_uuid': '46519267-81d0-4fb6-89dc-39fe8280ee79'
    },
    {
        'id': '9e3f9150-97ef-4a9a-9390-49b5f67423c0',
        'container_name': 'MSSP Example 5',
        'region': 'US East',
        'licensed_assets': 0,
        'licensed_assets_limit': -1,
        'licensed_apps': [],
        'notes': 'These are notes.',
        'logo_uuid': '5cc5d763-52a1-4943-a3b4-9bca84e9ae27'
    },
]


@responses.activate
def test_search(api):
    '''
    Test mssp accounts search method
    '''
    mock_resp = {
        'accounts': accounts_us_east,
        'pagination': {
            'total': len(accounts_us_east)
        }
    }
    responses.add(
        responses.POST,
        f'{MSSP_ACCOUNTS_URL}/search',
        json=mock_resp
    )
    fields = ['id', 'container_name', 'region', 'licensed_assets',
              'licensed_assets_limit', 'licensed_apps', 'notes', 'logo_uuid']
    resp = api.v3.mssp.accounts.search(fields=fields,
                                       filter=('region', 'eq', 'US EAST'),
                                       sort=[{
                                           'property': 'container_name',
                                           'order': 'asc'
                                       }])
    actual = []
    for account in resp:
        actual.append(account)

    expected = sorted(accounts_us_east, key=lambda i: i['container_name'])
    assert actual == expected
