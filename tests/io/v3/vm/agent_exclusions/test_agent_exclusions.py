'''
Test Cases For Agent Exclusions APIs
'''
import re
from datetime import datetime, timedelta

import pytest
import responses

BASE_URL: str = 'https://cloud.tenable.com/api/v3/agents'


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
    start_time: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Let's create test response for create agent exlusion endpoint
    test_response = {
        'id': 'c941af88-c514-4fdc-9657-ec72bd242ef7',
        'name': name,
        'description': description,
        'creation_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'last_modification_date':
            datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'core_updates_blocked': True,
        'schedule': {
            'starttime': start_time,
            'endtime': end_time,
            'enabled': enable,
            'rrules': {
                'freq': frequency,
                'interval': interval,
                'byweekday': ','.join(weekdays)
            }
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
            'rrules': {
                'freq': frequency,
                'interval': interval,
                'byweekday': ','.join(weekdays)
            }
        }
    }

    # Let's mock the response for create agent exclusion API endpoint
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/exclusions'),
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
        re.compile(f'{BASE_URL}/exclusions/{exclusion_id}'),
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
        'id': exclusion_id,
        'name': 'Example Weekly Exclusion',
        'description': '',
        'creation_date': '2021-12-24T09:57:28Z',
        'last_modification_date': '2021-12-24T09:57:28Z',
        'core_updates_blocked': True,
        'schedule': {
            'starttime': '2021-12-24T09:57:28Z',
            'endtime': '2021-12-24T10:57:28Z',
            'enabled': True,
            'rrules': {
                'freq': 'WEEKLY',
                'interval': '1',
                'byweekday': 'MO,WE,FR'
            }
        }
    }

    # Let's mock the response for agent exlusion details endpoint
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/exclusions/{exclusion_id}'),
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
    new_name: str = 'Test Edit Method 1'

    # Let's create sample response for agent exclusion edit endpoint
    test_response = {
        'id': 'c941af88-c514-4fdc-9657-ec72bd242ef7',
        'name': new_name,
        'description': '',
        'creation_date': '2021-12-24T09:57:28Z',
        'last_modification_date': '2021-12-24T09:57:28Z',
        'core_updates_blocked': True,
        'schedule': {
            'starttime': '2021-12-24T09:57:28Z',
            'endtime': '2021-12-24T10:57:28Z',
            'enabled': True,
            'rrules': {
                'freq': 'WEEKLY',
                'interval': '1',
                'byweekday': 'MO,WE,FR'
            }
        }
    }

    # Let's create sample payload for agent exclusion edit endpoint
    payload = {
        'name': new_name,
        'description': '',
        'schedule': {
            'enabled': True,
            'starttime': '2021-12-24T09:57:28Z',
            'endtime': '2021-12-24T10:57:28Z',
            'rrules': {
                'freq': 'WEEKLY',
                'interval': 1,
                'byweekday': 'MO,WE,FR'
            }
        }
    }

    # Let's mock the response for agent exclusion details endpoint
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/exclusions/{exclusion_id}'),
        json={
            'id': 'c941af88-c514-4fdc-9657-ec72bd242ef7',
            'name': 'Example Weekly Exclusion',
            'description': '',
            'creation_date': '2021-12-24T09:57:28Z',
            'last_modification_date': '2021-12-24T09:57:28Z',
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-12-24T09:57:28Z',
                'endtime': '2021-12-24T10:57:28Z',
                'enabled': True,
                'rrules': {
                    'freq': 'WEEKLY',
                    'interval': '1',
                    'byweekday': 'MO,WE,FR'
                }
            }
        }
    )

    # Let's mock the response for agent exclusion edit endpoint
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/exclusions/{exclusion_id}'),
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
    with pytest.raises(NotImplementedError):
        api.v3.vm.agent_exclusions.search()
