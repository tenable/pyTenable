'''
Test cases for exclusion API
'''
import os
from datetime import datetime, timedelta

import pytest
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL: str = 'https://cloud.tenable.com/api/v3/exclusions'
FILE_BASE_URL: str = 'https://cloud.tenable.com/api/v3/file'
TIMEZONE_URL: str = 'https://cloud.tenable.com/scans/timezones'


@responses.activate
def test_create(api):
    '''
    Test case for create exclusion API endpoint
    '''
    name: str = 'Exclusion Test Example'
    members: list = ['127.0.0.1']
    start_time: datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    end_time: datetime = (
        datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    enabled: bool = True
    freq: str = 'MONTHLY'
    bymonthday: int = datetime.today().day
    interval: int = 1
    timezone: str = 'Etc/UTC'
    # Let's create response for create endpoint
    test_response: dict = {
        'schedule': {
            'endtime': end_time,
            'enabled': enabled,
            'rrules': {
                'freq': freq,
                'interval': interval,
                'bymonthday': bymonthday
            },
            'timezone': timezone,
            'starttime': start_time
        },
        'network_id': '00000000-0000-0000-0000-000000000000',
        'last_modification_date': '2022-01-24T08:46:34Z',
        'creation_date': '2022-01-24T08:46:34Z',
        'members': ','.join(members),
        'description': None,
        'name': name,
        'id': 21
    }
    # Let's create payload for create endpoint
    payload: dict = {
        'members': ','.join(members),
        'name': name,
        'network_id': '00000000-0000-0000-0000-000000000000',
        'schedule': {
            'enabled': enabled,
            'starttime': start_time,
            'rrules': {
                'freq': freq,
                'bymonthday': bymonthday,
                'interval': interval
            },
            'timezone': timezone,
            'endtime': end_time
        }
    }
    # Let's register the response for timezone API
    responses.add(
        responses.GET,
        TIMEZONE_URL,
        json={
            'timezones': [
                {
                    'name': 'Africa/Addis_Ababa',
                    'value': 'Africa/Addis_Ababa'
                },
                {
                    'name': 'Etc/UTC',
                    'value': 'Etc/UTC'
                }
            ]
        }
    )
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
        frequency=freq,
        day_of_month=bymonthday,
        enabled=True
    )

    assert isinstance(res, dict)
    assert name == res['name']
    assert members == res['members'].split(',')

    with pytest.raises(TypeError):
        api.v3.vm.exclusions.create(
            name=name,
            members=members,
            enabled="False"
        )


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
            'endtime': '2022-01-09 16:44:32',
            'enabled': True,
            'rrules': {
                'freq': 'WEEKLY',
                'interval': 2,
                'byweekday': 'MO,WE,FR'
            },
            'timezone': 'Etc/UTC',
            'starttime': '2022-01-09 15:44:32'
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
    new_name: str = 'Test Edit method'

    # Let's create reasponse for edit endpoint
    test_response: dict = {
        "schedule": {
            "endtime": "2022-01-07 13:11:39",
            "enabled": True,
            "rrules": {
                "freq": "WEEKLY",
                "interval": 1,
                "byweekday": "MO"
            },
            "timezone": "Etc/UTC",
            "starttime": "2022-01-07 12:11:39"
        },
        "network_id": "00000000-0000-0000-0000-000000000000",
        "last_modification_date": "2022-01-07 12:11:39",
        "creation_date": "2022-01-07 12:11:39",
        "members": "127.0.0.1",
        "description": "Example for weekly exlusion",
        "name": new_name,
        "id": exclusion_id
    }

    # Let's create payload for edit endpoint
    payload: dict = {
        "schedule": {
            "timezone": "Etc/UTC",
            "starttime": "2022-01-07 12:11:39",
            "enabled": True,
            "rrules": {
                "freq": "WEEKLY",
                "interval": 1,
                "byweekday": "MO"
            },
            "endtime": "2022-01-07 13:11:39"
        },
        "description": "Example for weekly exlusion",
        "network_id": "00000000-0000-0000-0000-000000000000",
        "members": "127.0.0.1",
        "name": new_name
    }

    # Let's register the response for timezone API
    responses.add(
        responses.GET,
        TIMEZONE_URL,
        json={
            'timezones': [
                {
                    'name': 'US/Arizona',
                    'value': 'US/Arizona'
                },
                {
                    'name': 'Etc/UTC',
                    'value': 'Etc/UTC'
                }
            ]
        }
    )
    # Let's register mock response for details endpoint
    responses.add(
        responses.GET,
        f'{BASE_URL}/{exclusion_id}',
        json={
            "schedule": {
                "endtime": "2022-01-07 13:11:39",
                "enabled": True,
                "rrules": {
                    "freq": "WEEKLY",
                    "interval": 1,
                    "byweekday": "MO"
                },
                "timezone": "Etc/UTC",
                "starttime": "2022-01-07 12:11:39"
            },
            "network_id": "00000000-0000-0000-0000-000000000000",
            "last_modification_date": '2022-01-07T12:11:39Z',
            "creation_date": '2022-01-07T12:11:39Z',
            "members": "127.0.0.1",
            "description": "Example for weekly exlusion",
            "name": "Weekly Exclusion Example",
            "id": exclusion_id
        }
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

    assert len(list(iterator)) == test_response['pagination']['total']

    iterator = api.v3.vm.exclusions.search(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.exclusions.search(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(resp, Response)
