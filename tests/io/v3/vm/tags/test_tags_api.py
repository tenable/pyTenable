'''
Test Agents
'''
import re

import pytest
import responses

BASE_URL = 'https://cloud.tenable.com/tags'


@responses.activate
def test_create_category(api):
    '''
    Test case for tags create_category method
    '''
    name: str = 'Location'
    description: str = 'category for particuler location'
    test_response = {
        'id': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'created_at': '2021-12-28T08:42:39.101Z',
        'created_by': 'jyoti.patel@crestdatasys.com',
        'updated_at': '2021-12-28T08:42:39.101Z',
        'updated_by': 'jyoti.patel@crestdatasys.com',
        'name': name,
        'description': description,
        'reserved': False
    }
    payload: dict = {
        'name': name,
        'description': description
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/categories'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.tags.create_category(
        name=name,
        description=description
    )
    assert isinstance(res, dict)
    assert 'id' in list(res.keys())
    assert res['name'] == name
    assert res['description'] == description


@responses.activate
def test_details_category(api):
    '''
    Test case for tags details_category method
    '''
    category_id: str = '54595f6e-648c-4570-b967-9b4e6a947634'
    test_response = {
        'id': category_id,
        'created_at': '2021-12-29T17:01:05.462Z',
        'created_by': 'jyoti.patel@crestdatasys.com',
        'updated_at': '2021-12-29T17:01:05.462Z',
        'updated_by': 'jyoti.patel@crestdatasys.com',
        'name': 'sample category 1',
        'description': 'sample category for testting purpose',
        'reserved': False,
        'value_count': 0
    }
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/categories/{category_id}'),
        json=test_response
    )
    res = api.v3.vm.tags.details_category(
        category_id=category_id
    )
    assert isinstance(res, dict)
    assert res['id'] == category_id


@responses.activate
def test_edit_category(api):
    '''
    Test case for tags edit_category method
    '''
    name: str = 'Test Location'
    description: str = 'Test location category for tags'
    category_id: str = '54595f6e-648c-4570-b967-9b4e6a947634'
    test_response = {
        'id': category_id,
        'created_at': '2021-12-29T17:01:05.462Z',
        'created_by': 'jyoti.patel@crestdatasys.com',
        'updated_at': '2021-12-29T17:44:11.706Z',
        'updated_by': 'jyoti.patel@crestdatasys.com',
        'name': name,
        'description': description,
        'reserved': False,
        'value_count': 0
    }
    payload: dict = {
        'name': name,
        'description': description
    }
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/categories/{category_id}'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.tags.edit_category(
        category_id=category_id,
        name=name,
        description=description
    )
    assert isinstance(res, dict)
    assert res['id'] == category_id
    assert res['name'] == name
    assert res['description'] == description


@responses.activate
def test_delete_category(api):
    '''
    Test case for tags delete_category method
    '''
    category_id: str = '54595f6e-648c-4570-b967-9b4e6a947634'
    responses.add(
        responses.DELETE,
        re.compile(f'{BASE_URL}/categories/{category_id}')
    )
    res = api.v3.vm.tags.delete_category(
        category_id=category_id
    )
    assert res is None


@responses.activate
def test_details(api):
    '''
    Test case for tags details method
    '''
    value_id: str = '60bfce80-f695-4ed0-bd47-ec9e5b2946e5'
    test_response: dict = {
        'id': value_id,
        'created_at': '2021-12-30T05:34:46.626Z',
        'created_by': 'jyoti.patel@crestdatasys.com',
        'updated_at': '2021-12-30T05:34:46.626Z',
        'updated_by': 'jyoti.patel@crestdatasys.com',
        'category_uuid': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'value': 'Chicago',
        'type': 'static',
        'category_name': 'Location',
        'category_description': 'category for particuler location',
        'assignment_count': 0,
        'access_control': {
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'defined_domain_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'all_users_permissions': [],
            'current_domain_permissions': [
                {
                    'id': 'e9f23194-adb7-4c02-8632-615c694c787e',
                    'name': 'jyoti.patel@crestdatasys.com',
                    'type': 'USER',
                    'permissions': [
                        'CAN_USE',
                        'CAN_EDIT'
                    ]
                }
            ],
            'version': 0
        },
        'saved_search': False
    }
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/values/{value_id}'),
        json=test_response
    )
    res = api.v3.vm.tags.details(
        value_id=value_id
    )
    assert isinstance(res, dict)
    assert res['id'] == value_id


@responses.activate
def test_delete_singluer_tag_value(api):
    '''
    Test case for tags delete method for sigluer tag value
    '''
    value_id: str = '60bfce80-f695-4ed0-bd47-ec9e5b2946e5'
    responses.add(
        responses.DELETE,
        re.compile(f'{BASE_URL}/values/{value_id}')
    )
    res = api.v3.vm.tags.delete(
        value_id
    )
    assert res is None


@responses.activate
def test_delete_multiple_tag_values(api):
    '''
    Test case for tags delete method for multiple tag value
    '''
    payload: dict = {
        'values': [
            '60bfce80-f695-4ed0-bd47-ec9e5b2946e5',
            '60bfce80-f695-4ed0-bd47-ec9e5b2946e5',
            '60bfce80-f695-4ed0-bd47-ec9e5b2946e5'
        ]
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/values/delete-requests'),
        match=[responses.matchers.json_params_matcher(payload)]
    )
    res = api.v3.vm.tags.delete(
        '60bfce80-f695-4ed0-bd47-ec9e5b2946e5',
        '60bfce80-f695-4ed0-bd47-ec9e5b2946e5',
        '60bfce80-f695-4ed0-bd47-ec9e5b2946e5'
    )
    assert res is None


@responses.activate
def test_assign(api):
    '''
    Test case for tags assign method
    '''
    asset_ids: list = ['60bfce80-f695-4ed0-bd47-ec9e5b2946e5']
    tag_ids: list = ['54595f6e-648c-4570-b967-9b4e6a947634']
    payload: dict = {
        'action': 'add',
        'assets': asset_ids,
        'tags': tag_ids
    }
    test_response: dict = {
        'job_id': '62210d02a7056d0297f50a8ddfbd549eaef1d0bc94e1ea3fad09'
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/assets/assignments'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.tags.assign(
        assets=asset_ids,
        tags=tag_ids
    )
    assert isinstance(res, str)
    assert test_response['job_id'] == res


@responses.activate
def test_unassign(api):
    '''
    Test case for tags unassign method
    '''
    asset_ids: list = ['60bfce80-f695-4ed0-bd47-ec9e5b2946e5']
    tag_ids: list = ['54595f6e-648c-4570-b967-9b4e6a947634']
    payload: dict = {
        'action': 'remove',
        'assets': asset_ids,
        'tags': tag_ids
    }
    test_response: dict = {
        'job_id': '62210d02a7056d0297f50a8ddfbd549eaef1d0bc94e1ea3fad09'
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/assets/assignments'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.tags.unassign(
        assets=asset_ids,
        tags=tag_ids
    )
    assert isinstance(res, str)
    assert test_response['job_id'] == res


@responses.activate
def test_list_asset_tag(api):
    '''
    Test case for tags list_asset_tag method
    '''
    asset_id: str = 'c712813b-ce97-4d48-b9f2-b51bfa636dd7'

    test_response: dict = {
        "tags": [{
            "value_id": "173c3f3c-cb25-4f35-97e8-26b83f50c38d",
            "category_name": "location",
            "asset_id": asset_id,
            "created_at": "2018-12-31T16:29:40.606Z",
            "source": "static",
            "value": "Chicago",
            "created_by": "8ba8728a-04c8-4694-bdb3-c94e04ba3ccf",
            "category_id": "e50a526c-966f-4b80-a641-6dd359b8202e"
        }, {
            "value_id": "6c25f771-61b6-412d-8e10-1778203f14c8",
            "category_name": "threat",
            "asset_id": asset_id,
            "created_at": "2018-12-31T16:29:40.606Z",
            "source": "static",
            "value": "wannacry",
            "created_by": "8ba8728a-04c8-4694-bdb3-c94e04ba3ccf",
            "category_id": "c9f13d31-e9f7-40e6-9830-3c770e800675"
        }]
    }
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/assets/{asset_id}/assignments'),
        json=test_response
    )
    res = api.v3.vm.tags.list_asset_tag(asset_id=asset_id)
    assert isinstance(res, dict)
    for tag in res['tags']:
        assert tag['asset_id'] == asset_id


@responses.activate
def test_create(api):
    '''
    Test case for tags create method
    '''
    payload: dict = {
        'category_name': 'Location',
        'value': 'Ahmedabad',
        'filter_type': 'and',
        'access_control': {
            'all_users_permissions': [
                'CAN_EDIT'
            ],
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS'
            ],
            'current_domain_permissions': [
                {
                    'permissions': [
                        'CAN_EDIT'
                    ],
                    'name': 'user@company.com',
                    'type': 'USER',
                    'id': 'c2f2d080-ac2b-4278-914b-29f148682ee1'
                }
            ]
        }
    }
    test_response: dict = {
        'uuid': '8df056ea-a569-46a7-a443-fb58b34f20e6',
        'created_at': '2022-01-05T10:39:35.775Z',
        'created_by': 'jyoti.patel@crestdatasys.com',
        'updated_at': '2022-01-05T10:39:35.775Z',
        'updated_by': 'jyoti.patel@crestdatasys.com',
        'category_uuid': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'value': 'Ahmedabad',
        'type': 'static',
        'category_name': 'Location',
        'category_description': 'category for particuler location',
        'assignment_count': 0,
        'access_control': {
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'defined_domain_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'all_users_permissions': [

            ],
            'current_domain_permissions': [
                {
                    'id': 'e9f23194-adb7-4c02-8632-615c694c787e',
                    'name': 'jyoti.patel@crestdatasys.com',
                    'type': 'USER',
                    'permissions': [
                        'CAN_USE',
                        'CAN_EDIT'
                    ]
                }
            ],
            'version': 0
        },
        'saved_search': False
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/values'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.tags.create(
        category='Location',
        value='Ahmedabad',
        all_users_permissions=['CAN_EDIT'],
        current_domain_permissions=[(
            'c2f2d080-ac2b-4278-914b-29f148682ee1',
            'user@company.com',
            'USER',
            ['CAN_EDIT']
        )]
    )
    assert isinstance(res, dict)
    assert payload['value'] == res['value']


@responses.activate
def test_edit(api):
    '''
    Test case for tags edit method
    '''
    value_id: str = '8df056ea-a569-46a7-a443-fb58b34f20e6'
    value: str = 'New York'

    payload: dict = {
        'value': value,
        'filter_type': 'and',
        'access_control': {
            'all_users_permissions': [

            ],
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'defined_domain_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'version': 0,
            'current_domain_permissions': [
                {
                    'permissions': [
                        'CAN_USE',
                        'CAN_EDIT'
                    ],
                    'type': 'USER',
                    'name': 'jyoti.patel@crestdatasys.com',
                    'id': 'e9f23194-adb7-4c02-8632-615c694c787e'
                }
            ]
        }
    }

    # Response for edit tags value endpoint
    test_response: dict = {
        'id': value_id,
        'created_at': '2022-01-05T10:39:35.775Z',
        'created_by': 'jyoti.patel@crestdatasys.com',
        'updated_at': '2022-01-05T10:50:04.125Z',
        'updated_by': 'jyoti.patel@crestdatasys.com',
        'category_uuid': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'value': value,
        'type': 'static',
        'category_name': 'Location',
        'category_description': 'category for particuler location',
        'assignment_count': 0,
        'access_control': {
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'defined_domain_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'all_users_permissions': [

            ],
            'current_domain_permissions': [
                {
                    'id': 'e9f23194-adb7-4c02-8632-615c694c787e',
                    'name': 'jyoti.patel@crestdatasys.com',
                    'type': 'USER',
                    'permissions': [
                        'CAN_USE',
                        'CAN_EDIT'
                    ]
                }
            ],
            'version': 0
        },
        'saved_search': False
    }

    # Response for tag value details endpoint
    details_response: dict = {
        'id': value_id,
        'created_at': '2022-01-05T10:39:35.775Z',
        'created_by': 'jyoti.patel@crestdatasys.com',
        'updated_at': '2022-01-05T10:50:04.125Z',
        'updated_by': 'jyoti.patel@crestdatasys.com',
        'category_uuid': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'value': 'Ahmedabad',
        'type': 'static',
        'category_name': 'Location',
        'category_description': 'category for particuler location',
        'assignment_count': 0,
        'access_control': {
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'defined_domain_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'all_users_permissions': [

            ],
            'current_domain_permissions': [
                {
                    'id': 'e9f23194-adb7-4c02-8632-615c694c787e',
                    'name': 'jyoti.patel@crestdatasys.com',
                    'type': 'USER',
                    'permissions': [
                        'CAN_USE',
                        'CAN_EDIT'
                    ]
                }
            ],
            'version': 0
        },
        'saved_search': False
    }

    # let's Mock the response for tags details endpoint
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/values/{value_id}'),
        json=details_response
    )

    # Let's mock the response for edit tag value endpoint
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/values'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.tags.edit(
        value_id=value_id,
        value=value,
    )
    assert isinstance(res, dict)
    assert value_id == res['id']


def test_search(api):
    '''
    Test case for tags search method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.tags.search()


def test_search_categories(api):
    '''
    Test case for tags search_categories method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.tags.search_categories()
