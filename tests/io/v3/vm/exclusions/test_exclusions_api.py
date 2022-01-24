'''
Test cases for exclusion API
'''
import os
from datetime import datetime, timedelta

import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL: str = 'https://cloud.tenable.com/api/v3/exclusions'
FILE_BASE_URL: str = 'https://cloud.tenable.com/api/v3/file'


@responses.activate
def test_create(api):
    '''
    Test case for create exclusion API endpoint
    '''
    name: str = 'Weekly Exclusion'
    members: list = ['127.0.0.1']
    start_time: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')
    frequency: str = 'WEEKLY'
    interval: int = 2
    weekdays: list = ['MO', 'WE', 'FR']
    network_id: str = '00000000-0000-0000-0000-000000000000'
    description: str = 'Example for weekly exclusion'
    enabled: bool = True

    # Let's create response for create endpoint
    test_response: dict = {
        'schedule': {
            'endtime': end_time,
            'enabled': enabled,
            'rrules': {
                'freq': frequency,
                'interval': interval,
                'byweekday': ','.join(weekdays)
            },
            'starttime': start_time
        },
        'network_id': network_id,
        'last_modification_date': '2022-01-24T08:46:34Z',
        'creation_date': '2022-01-24T08:46:34Z',
        'members': ','.join(members),
        'description': description,
        'name': name,
        'id': 14
    }

    # Let's create payload for create endpoint
    payload: dict = {
        'members': ','.join(members),
        'schedule': {
            'starttime': start_time,
            'rrules': {
                'freq': frequency,
                'byweekday': ','.join(weekdays),
                'interval': interval
            },
            'enabled': enabled,
            'endtime': end_time
        },
        'description': description,
        'network_id': network_id,
        'name': name
    }

    # let's register mock response for create endpoint
    responses.add(
        responses.POST,
        f'{BASE_URL}',
        match=[matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.exclusions.create(
        name=name,
        members=members,
        start_time=start_time,
        end_time=end_time,
        description=description,
        frequency=frequency,
        interval=interval,
        weekdays=weekdays,
        enabled=enabled,
        network_id=network_id
    )

    assert isinstance(res, dict)
    assert name == res['name']
    assert members == res['members'].split(',')


@responses.activate
def test_delete(api):
    '''
    Test case for delete exclusion API endpoint
    '''
    exclusion_id: int = 10

    # Let's register mock response for delete endpoint
    responses.add(
        responses.DELETE,
        f'{BASE_URL}/{exclusion_id}'
    )

    res = api.v3.vm.exclusions.delete(exclusion_id=exclusion_id)

    assert res is None


@responses.activate
def test_details(api):
    '''
    Test case for details exclusion API endpoint
    '''
    exclusion_id: int = 1

    # Let's create sample response for details endpoint
    test_response: dict = {
        'schedule': {
            'endtime': '2022-01-09T16:44:32Z',
            'enabled': True,
            'rrules': {
                'freq': 'WEEKLY',
                'interval': 2,
                'byweekday': 'MO,WE,FR'
            },
            'timezone': 'Etc/UTC',
            'starttime': '2022-01-09T15:44:32Z'
        },
        'network_id': '00000000-0000-0000-0000-000000000000',
        'last_modification_date': '2022-01-24T08:46:34Z',
        'creation_date': '2022-01-24T08:46:34Z',
        'members': '127.0.0.1',
        'description': 'Example for weekly exclusion',
        'name': 'Weekly Exclusion',
        'id': exclusion_id
    }

    # Let's register the mock response for details endpoint
    responses.add(
        responses.GET,
        f'{BASE_URL}/{exclusion_id}',
        json=test_response
    )

    res = api.v3.vm.exclusions.details(exclusion_id=exclusion_id)

    assert isinstance(res, dict)
    assert res['id'] == exclusion_id


@responses.activate
def test_edit(api):
    '''
    Test case for edit exclusion API endpoint
    '''
    exclusion_id: int = 1
    new_name: str = 'New Name'

    # Let's create response for details endpoint
    details_res: dict = {
        'schedule': {
            'endtime': '2022-01-07T13:11:39Z',
            'enabled': True,
            'rrules': {
                'freq': 'DAILY',
                'interval': 1,
                'byweekday': 'MO'
            },
            'starttime': '2022-01-07T12:11:39Z'
        },
        'network_id': '00000000-0000-0000-0000-000000000000',
        'last_modification_date': '2022-01-24T08:46:34Z',
        'creation_date': '2022-01-24T08:46:34Z',
        'members': '127.0.0.1',
        'description': '',
        'name': 'Example 2',
        'id': 16
    }

    # Let's create reasponse for edit endpoint
    test_response: dict = {
        'schedule': {
            'endtime': '2022-01-07T13:11:39Z',
            'enabled': True,
            'rrules': {
                'freq': 'DAILY',
                'interval': 1
            },
            'starttime': '2022-01-07T12:11:39Z'
        },
        'network_id': '00000000-0000-0000-0000-000000000000',
        'last_modification_date': '2022-01-24T08:46:34Z',
        'creation_date': '2022-01-24T08:46:34Z',
        'members': '127.0.0.1',
        'description': '',
        'name': new_name,
        'id': exclusion_id
    }

    # Let's create payload for edit endpoint
    payload: dict = {
        'name': new_name,
        'description': '',
        'network_id': '00000000-0000-0000-0000-000000000000',
        'members': '127.0.0.1',
        'schedule': {
            'rrules': {
                'freq': 'DAILY',
                'interval': 1
            },
            'enabled': True,
            'endtime': '2022-01-07T13:11:39Z',
            'starttime': '2022-01-07T12:11:39Z'
        }
    }

    # Let's register mock response for details endpoint
    responses.add(
        responses.GET,
        f'{BASE_URL}/{exclusion_id}',
        json=details_res
    )

    # Let's register mock response for edit endpoint
    responses.add(
        responses.PUT,
        f'{BASE_URL}/{exclusion_id}',
        match=[matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.exclusions.edit(
        exclusion_id=exclusion_id,
        name=new_name
    )

    assert res['id'] == exclusion_id
    assert res['name'] == new_name
    assert isinstance(res, dict)


@responses.activate
def test_exclusions_import(api):
    '''
    Test case for import exclusion API endpoint
    '''

    filepath = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ), 'import_exclusion_test_file.csv'
    )

    # Let's create response for upload files endpoint
    uplaod_file_res: str = 'import_exclusion_test_file.csv'

    # Let's create payload for import exclusion endpoint
    payload: dict = {
        'file': uplaod_file_res
    }

    # Let's mock the response upload files endpoint
    responses.add(
        responses.POST,
        f'{FILE_BASE_URL}/upload',
        json={
            'fileuploaded': uplaod_file_res
        }
    )

    # let's mock the response for import exclusion endpoint
    responses.add(
        responses.POST,
        f'{BASE_URL}/import',
        match=[matchers.json_params_matcher(payload)]
    )

    with open(filepath) as fobj:
        res = api.v3.vm.exclusions.exclusions_import(fobj)

    assert res is None


@responses.activate
def test_search(api):
    '''
    Test case for search exclusion API endpoint
    '''
    test_response: dict = {
        'exclusions': [
            {
                'created_at': '2022-01-24T08:46:34Z',
                'description': 'This. is testing the micro frontend',
                'id': 6,
                'name': 'Micro Frontend Exclusion 1',
                'targets': '10.10.20.20',
                'type': 'ENABLED',
                'updated_at': '2022-01-24T08:46:34Z'
            },
            {
                'created_at': '2022-01-24T08:46:34Z',
                'description': 'This. istesting the micro frontend',
                'id': 7,
                'name': 'Micro Frontend Exclusion 2',
                'targets': '10.10.20.20',
                'type': 'ENABLED',
                'updated_at': '2022-01-24T08:46:34Z'
            }
        ],
        'pagination': {'total': 1, 'next': 'nextToken'}
    }

    fields: list = [
        'id',
        'name',
        'description',
        'targets',
        'type',
        'updated_at',
        'created_at'
    ]

    filter = {
        'and': [
            {
                'property': 'id',
                'operator': 'eq',
                'value': [6, 7]
            }
        ]
    }

    sort = [('id', 'asc')]

    # Let's create sample payload for search exclusion endpoint
    payload = {
        'fields': fields,
        'filter': filter,
        'limit': 200,
        'sort': [{'order': 'asc', 'property': 'id'}],
    }

    # Let's register the mock response for search endpoint
    responses.add(
        responses.POST,
        f'{BASE_URL}/search',
        json=test_response,
        match=[matchers.json_params_matcher(payload)],
    )

    iterator = api.v3.vm.exclusions.search(
        fields=fields, filter=filter, sort=sort, limit=200
    )
    assert isinstance(iterator, SearchIterator)

    exclusions_list = []
    for item in iterator:
        exclusions_list.append(item)
    assert len(exclusions_list) == test_response['pagination']['total']

    iterator = api.v3.vm.exclusions.search(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.exclusions.search(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(resp, Response)
