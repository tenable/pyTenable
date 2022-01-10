'''
Test cases for Exlusion API
'''
import os
from datetime import datetime, timedelta

import pytest
import responses
from responses import matchers

BASE_URL = 'https://cloud.tenable.com/api/v3/exclusions'
FILE_BASE_URL = 'https://cloud.tenable.com/api/v3/file'


@responses.activate
def test_create(api):
    '''
    Test case for create exlusion API endpoint
    '''
    name: str = "Weekly Exclusion"
    members: list = ["127.0.0.1"]
    start_time: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')
    frequency: str = 'WEEKLY'
    interval: int = 2
    weekdays: list = ['MO', 'WE', 'FR']
    network_id: str = '00000000-0000-0000-0000-000000000000'
    description: str = 'Example for weekly exlusion'
    enabled: bool = True

    # Let's create response for create exlusion endpoint
    test_response: dict = {
        "schedule": {
            "endtime": end_time,
            "enabled": enabled,
            "rrules": {
                "freq": frequency,
                "interval": interval,
                "byweekday": ','.join(weekdays)
            },
            "starttime": start_time
        },
        "network_id": network_id,
        "last_modification_date": 1641743194,
        "creation_date": 1641743194,
        "members": ','.join(members),
        "description": description,
        "name": name,
        "id": 14
    }

    # Let's create payload for create exclusion endpoint
    payload: dict = {
        "members": ','.join(members),
        "schedule": {
            "starttime": start_time,
            "rrules": {
                "freq": frequency,
                "byweekday": ','.join(weekdays),
                "interval": interval
            },
            "enabled": enabled,
            "endtime": end_time
        },
        "description": description,
        "network_id": network_id,
        "name": name
    }

    # let's mock response for create endpoint
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

    # Let's mock the response for delete endpoint
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

    test_response: dict = {
        "schedule": {
            "endtime": "2022-01-09T16:44:32Z",
            "enabled": True,
            "rrules": {
                "freq": "WEEKLY",
                "interval": 2,
                "byweekday": "MO,WE,FR"
            },
            "timezone": "Etc/UTC",
            "starttime": "2022-01-09T15:44:32Z"
        },
        "network_id": "00000000-0000-0000-0000-000000000000",
        "last_modification_date": 1641744295,
        "creation_date": 1641744295,
        "members": "127.0.0.1",
        "description": "Example for weekly exlusion",
        "name": "Weekly Exclusion",
        "id": exclusion_id
    }

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

    # Let's create test response for details exlcusion endpoint
    details_res: dict = {
        "schedule": {
            "endtime": "2022-01-07T13:11:39Z",
            "enabled": True,
            "rrules": {
                "freq": "DAILY",
                "interval": 1,
                "byweekday": "MO"
            },
            "starttime": "2022-01-07T12:11:39Z"
        },
        "network_id": "00000000-0000-0000-0000-000000000000",
        "last_modification_date": 1641751739,
        "creation_date": 1641747976,
        "members": "127.0.0.1",
        "description": "",
        "name": "Example 2",
        "id": 16
    }

    # Let's create reasponse for edit exclusion endpoint
    test_response: dict = {
        "schedule": {
            "endtime": "2022-01-07T13:11:39Z",
            "enabled": True,
            "rrules": {
                "freq": "DAILY",
                "interval": 1
            },
            "starttime": "2022-01-07T12:11:39Z"
        },
        "network_id": "00000000-0000-0000-0000-000000000000",
        "last_modification_date": 1641752036,
        "creation_date": 1641747976,
        "members": "127.0.0.1",
        "description": "",
        "name": new_name,
        "id": exclusion_id
    }

    # Let's create payload for mock response
    payload: dict = {
        "name": new_name,
        "description": "",
        "network_id": "00000000-0000-0000-0000-000000000000",
        "members": "127.0.0.1",
        "schedule": {
            "rrules": {
                "freq": "DAILY",
                "interval": 1
            },
            "enabled": True,
            "endtime": "2022-01-07T13:11:39Z",
            "starttime": "2022-01-07T12:11:39Z"
        }
    }

    # Let's mock the response for details endpoint
    responses.add(
        responses.GET,
        f'{BASE_URL}/{exclusion_id}',
        json=details_res
    )

    # Let's mock the response for edit endpoint
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
        ), 'import_exlusion_test_file.csv'
    )

    # Let's create response for upload files endpoint
    uplaod_file_res: str = 'import_exlusion_test_file.csv'

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
    Test case for search exlusion API endpoint
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.exclusions.search()
