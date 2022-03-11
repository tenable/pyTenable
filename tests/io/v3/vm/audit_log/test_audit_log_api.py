import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

AUDIT_LOG_BASE_URL = 'https://cloud.tenable.com/api/v3/audit-log/events/search'


@responses.activate
def test_search(api):
    '''
    Test vm audit_log search method
    '''
    api_res = {
        'events': [
            {
                'id': 'd2ccdf2b86f74d52aadbb21af0ce17c4',
                'action': 'audit.log.view',
                'actor_id': '01ad1230-8162-4bd5-b237-50f3636f2cb8',
                'actor_name': 'batman@tenable.com',
                'target_id': None,
                'target_name': None,
                'target_type': None,
                'description': 'GET /audit-log/v1/events',
                'is_anonymous': None,
                'is_failure': None,
                'fields': None,
                'received': '2021-10-27T05:21:58Z',
            }
        ],
        'pagination': {'total': 1, 'next': 'nextToken'},
    }
    fields = [
        'id',
        'action',
        'actor_id',
        'actor_name',
        'target_id',
        'target_name',
        'target_type',
        'description',
        'is_anonymous',
        'is_failure',
        'fields',
        'received',
    ]
    filter = {
        'and': [
            {
                'property': 'date',
                'operator': 'lt OR gt',
                'value': 'date_value',
            },
            {'property': 'actor_id', 'operator': 'eq', 'value': 'actor_value'},
            {
                'property': 'target_id',
                'operator': 'eq',
                'value': 'target_value',
            },
            {'property': 'action', 'operator': 'eq', 'value': 'action_value'},
        ]
    }
    sort = [('received', 'desc')]
    api_payload = {
        'fields': fields,
        'filter': filter,
        'limit': 200,
        'sort': [{'received': 'desc'}],
    }

    # Register expected response
    responses.add(
        responses.POST,
        AUDIT_LOG_BASE_URL,
        json=api_res,
        match=[matchers.json_params_matcher(api_payload)],
    )

    iterator = api.v3.vm.audit_log.search(
        fields=fields, filter=filter, sort=sort, limit=200
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == api_res['pagination']['total']

    iterator = api.v3.vm.audit_log.search(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.audit_log.search(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(resp, Response)
