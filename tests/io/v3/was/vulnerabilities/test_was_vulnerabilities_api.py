'''
Testing the WAS Vulnerabilities endpoints actions
'''
import pytest
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

VUL_BASE_URL = r'https://cloud.tenable.com/api/v3/findings/vulnerabilities'
BASE_URL = r'https://cloud.tenable.com'


@responses.activate
def test_get_details(api):
    '''
    Test the get_details method for WAS Vulnerabilities
    '''
    id = '00089a45-44a7-4620-bf9f-75ebedc6cc6c'
    # response = {
    #     'findings': [{
    #         'finding_id': id,
    #         'asset_name': 'www.google.com',
    #         'severity': 0,
    #         'state': 'ACTIVE',
    #         'last_observed': '2022-01-05T22:47:45.227Z'
    #     }],
    #     'pagination': {
    #         'total': 1,
    #         'next': 'nextToken'
    #     }
    # }
    # responses.add(
    #     responses.GET,
    #     f'{VUL_BASE_URL}/webapp/{id}',
    #     json=response
    # )

    # resp = api.v3.was.vulnerabilities.get_details(id)
    # assert resp == response
    with pytest.raises(NotImplementedError):
        api.v3.was.vulnerabilities.get_details(id)


@responses.activate
def test_search(api):
    '''
    Test the search functionality of Vulnerability API
    '''
    fields = [
        'asset_name',
        'severity',
        'plugin_id',
        'state',
        'last_observed',
        'finding_id'
    ]
    sort_payload = [
        {
            'property': 'last_observed',
            'order': 'desc'
        }
    ]

    sort = [("last_observed", "desc")]

    payload = {
        'fields': fields,
        'limit': 200,
        "sort": sort_payload
    }

    api_response = {
        'findings': [{
                'finding_id': 'a2d91989-2d02-4600-a31d-88d629e3b02d',
                'asset_name': 'www.google.com',
                'severity': 0,
                'state': 'ACTIVE',
                'last_observed': '2022-01-06T00:51:37.436Z'
            },
            {
                'finding_id': 'c010725b-4e62-4e66-8b29-853664a5a0c3',
                'asset_name': 'www.google.com',
                'severity': 1,
                'state': 'ACTIVE',
                'last_observed': '2022-01-06T00:51:37.436Z'
            }
        ],
        'pagination': {
            'total': 2,
            'next': 'nextToken'
        }
    }

    responses.add(
        responses.POST,
        f'{VUL_BASE_URL}/webapp/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.was.vulnerabilities.search(
        fields=fields, limit=200, sort=sort
    )
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.was.vulnerabilities.search(
        fields=fields, return_csv=True, sort=sort, limit=200
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.was.vulnerabilities.search(
        fields=fields, return_resp=True, limit=200, sort=sort
    )
    assert isinstance(resp, Response)
