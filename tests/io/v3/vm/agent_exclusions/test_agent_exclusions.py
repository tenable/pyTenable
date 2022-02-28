'''
Test Cases For Agent Exclusions APIs
'''
import re
from datetime import datetime, timedelta

import responses
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL: str = 'https://cloud.tenable.com/api/v3/agents/exclusions'
TIMEZONE_URL: str = 'https://cloud.tenable.com/api/v3/scans/timezones'


@responses.activate
def test_create(api):
    '''
    Test case for agent_exclusion create method
    '''
    name: str = 'Example Weekly Exclusion'
    description: str = 'This is a weekly exclusion example'
    enable: bool = True
    frequency: str = 'WEEKLY'
    interval: int = 1
    weekdays: list = ['MO', 'WE', 'FR']
    start_time: str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    end_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    timezone: str = 'UTC'

    # Let's create test response for create agent exlusion endpoint
    test_response = {
        'description': description,
        'name': name,
        'id': '534d4121-b55f-465c-bf79-0ff34d0b9a88',
        'creation_date': '2020-04-21T10:51:47+00:00',
        'last_modification_date': '2020-04-21T10:51:47+00:00',
        'core_updates_blocked': True,
        'schedule': {
            'starttime': '2020-04-21T20:30:00+07:00',
            'endtime': '2020-04-21T21:00:00+07:00',
            'enabled': True,
            'rrules': {
                'freq': 'ONETIME',
                'interval': '1'
            },
            'timezone': timezone
        }
    }

    # Let's create sample payload for create agent exclusion endpoint
    payload = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enable,
            'starttime': start_time,
            'endtime': end_time,
            'timezone': timezone,
            'rrules': {
                'freq': frequency,
                'interval': interval,
                'byweekday': ','.join(weekdays)
            }
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
                    'name': 'UTC',
                    'value': 'UTC'
                }
            ]
        }
    )

    # Let's mock the response for create agent exclusion API endpoint
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.agent_exclusions.create(
        frequency=frequency,
        name=name,
        start_time=start_time,
        enabled=enable,
        end_time=end_time,
        description=description,
        interval=interval,
        weekdays=weekdays
    )

    assert isinstance(res, dict)
    assert res['name'] == name


@responses.activate
def test_delete(api):
    '''
    Test case for agent_exclusion delete method
    '''
    exclusion_id: str = 'a3c9b1f5-ft45-cd4f-5fr3-6330694c9fb7'

    # Let's mock the Response for delete agent exlusion API endpoint
    responses.add(
        responses.DELETE,
        re.compile(f'{BASE_URL}/{exclusion_id}'),
    )

    res = api.v3.vm.agent_exclusions.delete(
        exclusion_id=exclusion_id
    )

    assert res is None


@responses.activate
def test_details(api):
    '''
    Test case for agent_exclusion details method
    '''
    exclusion_id: str = 'c941af88-c514-4fdc-9657-ec72bd242ef7'

    # Let's create sample response for agent exclusion details endpoint
    test_response = {
        'description': '',
        'name': 'sample-blackout-window-test',
        'id': exclusion_id,
        'creation_date': '2020-04-21T10:51:47-04:00',
        'last_modification_date': '2020-04-21T10:51:47-04:00',
        'core_updates_blocked': True,
        'schedule': {
            'starttime': '2020-04-21T20:30:00+07:00',
            'endtime': '2020-04-21T21:00:00+07:00',
            'enabled': True,
            'rrules': {
                'freq': 'ONETIME',
                'interval': '1'
            },
            'timezone': 'Indian/Christmas'
        }
    }

    # Let's mock the response for agent exlusion details endpoint
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/{exclusion_id}'),
        json=test_response
    )
    res = api.v3.vm.agent_exclusions.details(
        exclusion_id=exclusion_id
    )
    assert isinstance(res, dict)
    assert res['id'] == exclusion_id


@responses.activate
def test_edit(api):
    '''
    Test case for agent_exclusion edit method
    '''
    exclusion_id: str = 'c941af88-c514-4fdc-9657-ec72bd242ef7'
    new_name: str = 'Test Edit Method'

    # Let's create sample response for agent exclusion edit endpoint
    test_response = {
        'name': new_name,
        'id': exclusion_id,
        'creation_date': '2022-01-20T06:17:21-05:00',
        'last_modification_date': '2022-01-22T11:48:36-05:00',
        'core_updates_blocked': True,
        'schedule': {
            'enabled': True,
            'starttime': '2021-10-11T00:00:00-07:00',
            'endtime': '2021-12-12T00:00:00-07:00',
            'rrules': {
                'freq': 'MONTHLY',
                'interval': 1,
                'bymonthday': '5'
            },
            'timezone': 'US/Arizona'
        }
    }

    # Let's create sample payload for agent exclusion edit endpoint
    payload = {
        'name': 'Test Edit Method',
        'schedule': {
            'endtime': '2021-12-12 00:00:00',
            'starttime': '2021-10-11 00:00:00',
            'enabled': True,
            'timezone': 'US/Arizona',
            'rrules': {
                'freq': 'MONTHLY',
                'bymonthday': 5,
                'interval': 1
            }
        }
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
                    'name': 'UTC',
                    'value': 'UTC'
                }
            ]
        }
    )

    # Let's register the response for details endpoint
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/{exclusion_id}'),
        json={
            'name': 'Old Exclusion Name',
            'id': exclusion_id,
            'creation_date': '2022-01-20T06:17:21-05:00',
            'last_modification_date': '2022-01-22T11:48:36-05:00',
            'core_updates_blocked': True,
            'schedule': {
                'enabled': True,
                'starttime': '2021-10-11T00:00:00-07:00',
                'endtime': '2021-12-12T00:00:00-07:00',
                'rrules': {
                    'freq': 'MONTHLY',
                    'interval': 1,
                    'bymonthday': '5'
                },
                'timezone': 'US/Arizona'
            }
        }
    )

    # Let's mock the response for agent exclusion edit endpoint
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/{exclusion_id}'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.agent_exclusions.edit(
        exclusion_id=exclusion_id,
        name=new_name
    )

    assert isinstance(res, dict)
    assert res['name'] == new_name


@responses.activate
def test_search(api):
    '''
    Test case for agent_exclusion search method
    '''
    test_response: dict = {
        'exclusions': [
            {
                'schedule': {
                    'rrules': {
                        'freq': 'ONETIME',
                        'interval': '1'
                    },
                    'timezone': 'Indian/Christmas',
                    'endtime': '2020-05-11T23:00:00+07:00',
                    'starttime': '2020-05-11T20:30:00+07:00',
                    'enabled': True
                },
                'core_updates_blocked': True,
                'last_modification_date': '2020-05-11T11:35:14-04:00',
                'name': 'sample2222222-blackout-window',
                'description': '',
                'id': '6d6847dd-5478-45a0-bf30-1d53f4a5a926',
                'creation_date': '2020-05-11T11:35:14-04:00'
            }
        ],
        'pagination': {
            'next': 'nextToken',
            'total': 1
        }
    }

    fields: list = [
        'description',
        'name',
        'uuid',
        'creation_date',
        'last_modification_date',
        'id',
        'core_updates_blocked',
        'schedule'
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

    sort = [('creation_date', 'asc')]

    # Let's create sample payload for search exclusion endpoint
    payload = {
        'fields': fields,
        'filter': filter,
        'limit': 200,
        'sort': [{'creation_date': 'asc'}],
    }

    # Let's register the mock response for search endpoint
    responses.add(
        responses.POST,
        f'{BASE_URL}/search',
        json=test_response,
        match=[responses.matchers.json_params_matcher(payload)],
    )

    iterator = api.v3.vm.agent_exclusions.search(
        fields=fields, filter=filter, sort=sort, limit=200
    )
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == test_response['pagination']['total']

    iterator = api.v3.vm.agent_exclusions.search(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.agent_exclusions.search(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(resp, Response)
