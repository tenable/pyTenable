'''
Test for remediation scans endpoint
'''

import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

REM_SCANS_BASE_URL = r'https://cloud.tenable.com/api/v3/scans'
BASE_URL = r'https://cloud.tenable.com'


@responses.activate
def test_search(api):
    '''
    Test the search method
    '''
    fields = [
        'name',
        'type',
        'id'
    ]
    sort = [('creation_date', 'desc')]
    filters = ('status', 'eq', 'completed')

    payload = {
        'fields': fields,
        'limit': 200,
        'sort': [{'creation_date': 'desc'}],
        'filter': {
            'property': 'status',
            'operator': 'eq',
            'value': 'completed'
        }
    }

    api_response = {
        'scans': [
            {
                'type': 'ps',
                'id': '19270891-9d39-4087-ab1c-887fdf4f31d6',
                'permissions': 128,
                'enabled': False,
                'control': True,
                'read': False,
                'last_modification_date': '2026-01-06T00:51:37.436Z',
                'creation_date': '2026-01-06T00:51:37.436Z',
                'status': 'completed',
                'shared': False,
                'user_permissions': 128,
                'schedule_id':
                    'template-0aaf949f-dd1c-a1b6-8de9-7cb934568618f7d3e3bb22b45950', # noqa E501
                'wizard_id':
                    '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                'scan_creation_date': '2026-01-06T00:51:37.436Z',
                'owner': 'user1@example.com',
                'policy_id': '12760891-9d39-4087-ab1c-887fdf4f31d6',
                'name': 'Remediation Scan',
            }
        ],
        'pagination': {
            'total': 1,
            'next': 'nextToken'
        }
    }
    responses.add(
        responses.POST,
        f'{REM_SCANS_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.vm.remediation_scans.search(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.vm.remediation_scans.search(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.remediation_scans.search(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)


@responses.activate
def test_create(api):
    '''
    Test for create method
    '''
    # todo => add more params for high test coverage later
    id = 'template-54910541-1016-191c-f92d-fe58f5455d40bbac8a568ec40c26'
    create_resp_data = {
        'scan': {
            'tag_type': None,
            'container_id': '7a818eb1-8351-4795-99b0-9610c8954cb4',
            'owner_id': '68f1b7a3-caf0-4ef6-87a5-2d31338ead34',
            'id':
                'template-54910541-1016-191c-f92d-fe58f5455d40bbac8a568ec40c26',  # noqa: E501
            'name': 'remediationMultiple',
            'description': 'string',
            'policy_id': 602,
            'scanner_id':
                '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': False,
            'include_aggregate': True,
            'scan_time_window': 0,
            'custom_targets': '192.0.2.1/24',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 1,
            'starttime': None,
            'rrules': None,
            'timezone': None,
            'notification_filters': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'user@example.com',
            'last_modification_date': '2019-12-31T20:50:23.635Z',
            'creation_date': '2019-12-31T20:50:23.635Z',
            'type': 'public',
        }
    }

    policy_template_res = [
        {
            'unsupported': False,
            'cloud_only': False,
            'desc': 'Remote and local checks for CVE-2017-5689.',
            'order': 8,
            'subscription_only': False,
            'is_was': 'None',
            'title': 'Intel AMT Security Bypass',
            'is_agent': 'None',
            'uuid': '3f514e0e-66e0-8ea2-b6e7-d2d86b526999a93a89944d19e1f1',
            'icon':
                'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48c3'
                'ZnIHZlcnNpb249IjEuMSIgaWQ9ImJhc2ljV2ViQXBwU2NhbiIge'
                'G1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp'
                '4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeD0i'
                'MHB4IiB5PSIwcHgiIHZpZXdCb3g9IjAgMCAxNiAxNiIgc3R5bG'
                'U9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMTYgMTY7'
                'IiB4bWw6c3BhY2U9InByZXNlcnZlIj48c3R5bGUgdHlwZT0idGV4dC9jc'
                '3MiPi5zdDB7ZmlsbDojREJEOUQ2O30uc3Qxe2ZpbGw6I0FBQTlBQTt9LnN0M'
                'ntmaWxsOiM3Nzg1OTI7fS5zdDN7ZmlsbDojNDM1MzYzO30uc3Q0e2ZpbGw'
                '6IzI2Mzc0NTt9LnN0NXtmaWxsOiNGMzZDM0U7fS5zdDZ7ZmlsbDojQUU0N'
                'TI1O30uc3Q3e2ZpbGw6I0RCRTBFMTt9LnN0OHtmaWxsOiNGRkZGRkY7fTwv'
                'c3R5bGU+PGcgaWQ9Im5vZGVzIj48ZyBpZD0ibm9kZSI+PHJlY3QgeD0iNCI'
                'geT0iMSIgY2xhc3M9InN0MCIgd2lkdGg9IjEiIGhlaWdodD0iMiIvPjxyZW'
                'N0IHg9IjQiIHk9IjIiIGNsYXNzPSJzdDEiIHdpZHRoPSIxIiBoZWlnaHQ9I'
                'jEiLz48L2c+PGcgaWQ9Im5vZGVfMV8iPjxyZWN0IHg9IjUuNzUiIHk9IjEi'
                'IGNsYXNzPSJzdDAiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiLz48cmVjdCB4PSI1',
            'manager_only': False,
            'name': 'advanced'
        },
        {
            'unsupported': False,
            'cloud_only': False,
            'desc': 'A full system scan suitable for any host.',
            'order': 1,
            'subscription_only': False,
            'is_was': 'None',
            'title': 'Basic Network Scan',
            'is_agent': 'None',
            'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
            'icon':
                'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48IURPQ1RZU'
                'EUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi'
                '8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiP',
            'manager_only': False,
            'name': 'basic'
        }
    ]

    responses.add(
        responses.POST,
        url=f'{REM_SCANS_BASE_URL}/remediation',
        json=create_resp_data
    )
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/editor/policy/templates',
        json={'templates': policy_template_res}
    )

    resp = api.v3.vm.remediation_scans.create_remediation_scan(
        id=id,
        name='Create Remediation Scan',
        description='Remediation scan created',
        scanner_id='10167769',
        scan_time_window=10,
        targets=['127.0.0.1:3000'],
        template='advanced',
        credentials={},
        compliance={},
        enabled_plugins=[110, 120, 130]
    )
    assert resp['id'] == id
