'''
Test case for Tags API
'''
import re

import responses
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL = 'https://cloud.tenable.com/api/v3/tags'


@responses.activate
def test_create(api):
    '''
    Test case for tags create method
    '''
    category_name: str = 'Category_1'
    category_description: str = 'Description for category'
    value: str = 'Value_1'
    description: str = 'Description for Value'
    current_user_permissions: list = ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
    all_users_permissions: list = ['CAN_EDIT']
    current_domain_permissions: list = [
        {
            'id': 'c2f2d080-ac2b-4278-914b-29f148682ee1',
            'name': 'user@company.com',
            'type': 'USER',
            'permissions': [
                'CAN_EDIT'
            ]
        }
    ]

    # Let's create sample payload for api endpoint
    payload: dict = {
        'description': description,
        'value': value,
        'access_control': {
            'current_domain_permissions': current_domain_permissions,
            'all_users_permissions': all_users_permissions,
            'current_user_permissions': current_user_permissions
        },
        'category_description': category_description,
        'category_name': category_name
    }

    # Let's create sample response for api endpoint
    test_response: dict = {
        'id': 'f8aae2b3-e020-4cbb-a6ef-1e91f93de6da',
        'created_at': '2022-01-13T12:56:43.119Z',
        'created_by': 'user@company.com',
        'updated_at': '2022-01-13T12:56:43.119Z',
        'updated_by': 'user@company.com',
        'category_id': 'c247e05a-22c8-4804-b43e-f245d1952001',
        'value': value,
        'description': description,
        'type': 'static',
        'product': 'IO',
        'category_name': category_name,
        'category_description': category_description,
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
                    'name': 'user@company.com',
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

    # Let's register the mock response for create tag value endpoint
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/values'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.tags.create(
        category=category_name,
        value=value,
        description=description,
        category_description=category_description,
        all_users_permissions=all_users_permissions,
        current_domain_permissions=current_domain_permissions
    )
    assert isinstance(res, dict)
    assert res['value'] == payload['value']


@responses.activate
def test_create_category(api):
    '''
    Test case for tags create_category method
    '''
    name: str = 'Location'
    description: str = 'category for particular location'

    # Let's create sample payload for api endpoint
    payload: dict = {
        'name': name,
        'description': description
    }

    # Let's create sample response for api endpoint
    test_response = {
        'id': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'created_at': '2021-12-28T08:42:39.101Z',
        'created_by': 'user@company.com',
        'updated_at': '2021-12-28T08:42:39.101Z',
        'updated_by': 'user@company.com',
        'name': name,
        'description': description,
        'reserved': False
    }

    # Let's register the response for create tag category endpoint
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
    assert res['name'] == name
    assert res['description'] == description


@responses.activate
def test_delete_singular_tag_value(api):
    '''
    Test case for tags delete method for singular tag value
    '''
    value_id: str = '00000000-0000-0000-0000-000000000000'

    # Let's register the response for delete tag value endpoint
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
    # Let's create sample payload for api
    payload: dict = {
        'values': [
            '00000000-0000-0000-0000-000000000000',
            '00000000-0000-0000-0000-000000000001'
        ]
    }

    # Let's register the response for delete tag value endpoint
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/values/delete-requests'),
        match=[responses.matchers.json_params_matcher(payload)]
    )

    res = api.v3.vm.tags.delete(
        '00000000-0000-0000-0000-000000000000',
        '00000000-0000-0000-0000-000000000001'
    )

    assert res is None


@responses.activate
def test_delete_category(api):
    '''
    Test case for tags delete_category method
    '''
    category_id: str = '00000000-0000-0000-0000-000000000000'

    # Let's register the response for delete tags category endpoint
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

    # Let's create sample response for api endpoint
    test_response: dict = {
        'id': value_id,
        'created_at': '2021-12-30T05:34:46.626Z',
        'created_by': 'user@company.com',
        'updated_at': '2021-12-30T05:34:46.626Z',
        'updated_by': 'user@company.com',
        'category_id': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
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
                    'name': 'user@company.com',
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

    # Let's register the response for tags value details endpoint
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
def test_details_category(api):
    '''
    Test case for tags details_category method
    '''
    category_id: str = '54595f6e-648c-4570-b967-9b4e6a947634'

    # Let's create sample response for api endpoint
    test_response = {
        'id': category_id,
        'created_at': '2021-12-29T17:01:05.462Z',
        'created_by': 'user@company.com',
        'updated_at': '2021-12-29T17:01:05.462Z',
        'updated_by': 'user@company.com',
        'name': 'sample category 1',
        'description': 'sample category for testting purpose',
        'reserved': False,
        'value_count': 0
    }

    # Let's register the response for tags category details endpoint
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
def test_edit(api):
    '''
    Test case for tags edit method
    '''
    value_id: str = '8df056ea-a569-46a7-a443-fb58b34f20e6'
    value: str = 'New York'

    # Let's create sample payload for api endpoint
    payload: dict = {
        'value': value,
        'access_control': {
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ],
            'all_users_permissions': [],
            'current_domain_permissions': [
                {
                    'id': 'e9f23194-adb7-4c02-8632-615c694c787e',
                    'type': 'USER',
                    'name': 'user@company.com',
                    'permissions': [
                        'CAN_USE',
                        'CAN_EDIT'
                    ]
                }
            ],
            'version': 0,
            'defined_domain_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS',
                'CAN_USE'
            ]
        }
    }

    # Let's create sample response for api endpoint
    test_response: dict = {
        'id': value_id,
        'created_at': '2022-01-13T08:56:21.715Z',
        'created_by': 'user@company.com',
        'updated_at': '2022-01-13T15:45:20.939Z',
        'updated_by': 'user@company.com',
        'category_id': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'value': value,
        'type': 'dynamic',
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
                    'name': 'user@company.com',
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

    # Let's create response for tags value details endpoint
    details_response: dict = {
        'id': value_id,
        'created_at': '2022-01-13T08:56:21.715Z',
        'created_by': 'user@company.com',
        'updated_at': '2022-01-13T15:45:20.939Z',
        'updated_by': 'user@company.com',
        'category_id': '4c5f6aaf-22fe-458d-a7a3-76c60e90147a',
        'value': 'New York',
        'type': 'dynamic',
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
                    'name': 'user@company.com',
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

    # Let's register the mock response for tags value details endpoint
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/values/{value_id}'),
        json=details_response
    )

    # Let's register the mock response for tags value edit endpoint
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


@responses.activate
def test_edit_category(api):
    '''
    Test case for tags edit_category method
    '''
    name: str = 'Test Location'
    description: str = 'Test location category for tags'
    category_id: str = '54595f6e-648c-4570-b967-9b4e6a947634'

    # Let's create sample response for api endpoint
    test_response = {
        'id': category_id,
        'created_at': '2021-12-29T17:01:05.462Z',
        'created_by': 'user@company.com',
        'updated_at': '2021-12-29T17:44:11.706Z',
        'updated_by': 'user@company.com',
        'name': name,
        'description': description,
        'reserved': False,
        'value_count': 0
    }

    # Let's create sample payload for api endpoint
    payload: dict = {
        'name': name,
        'description': description
    }

    # Let's register the response for tags category edit endpoint
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
    assert res['name'] == name
    assert res['description'] == description


@responses.activate
def test_list_asset_tag(api):
    '''
    Test case for tags list_asset_tag method
    '''
    asset_id: str = 'c712813b-ce97-4d48-b9f2-b51bfa636dd7'

    # Let's create sample response for api endpoint
    test_response: dict = {
        'tags': [{
            'value_id': '173c3f3c-cb25-4f35-97e8-26b83f50c38d',
            'category_name': 'location',
            'asset_id': asset_id,
            'created_at': '2018-12-31T16:29:40.606Z',
            'source': 'static',
            'value': 'Chicago',
            'created_by': '8ba8728a-04c8-4694-bdb3-c94e04ba3ccf',
            'category_id': 'e50a526c-966f-4b80-a641-6dd359b8202e'
        }, {
            'value_id': '6c25f771-61b6-412d-8e10-1778203f14c8',
            'category_name': 'threat',
            'asset_id': asset_id,
            'created_at': '2018-12-31T16:29:40.606Z',
            'source': 'static',
            'value': 'wannacry',
            'created_by': '8ba8728a-04c8-4694-bdb3-c94e04ba3ccf',
            'category_id': 'c9f13d31-e9f7-40e6-9830-3c770e800675'
        }]
    }

    # Let's register the response for api endpoint
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
def test_assign(api):
    '''
    Test case for tags assign method
    '''
    asset_ids: list = ['60bfce80-f695-4ed0-bd47-ec9e5b2946e5']
    tag_ids: list = ['54595f6e-648c-4570-b967-9b4e6a947634']

    # Let's create sample payload for api endpoint
    payload: dict = {
        'action': 'add',
        'assets': asset_ids,
        'tags': tag_ids
    }

    # Let's create sample response for api endpoint
    test_response: dict = {
        'job_id': '62210d02a7056d0297f50a8ddfbd549eaef1d0bc94e1ea3fad09'
    }

    # Let's register the response to api endpoint
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

    # Let's create sample payload for api endpoint
    payload: dict = {
        'action': 'remove',
        'assets': asset_ids,
        'tags': tag_ids
    }

    # Let's create sample response for api endpoint
    test_response: dict = {
        'job_id': '62210d02a7056d0297f50a8ddfbd549eaef1d0bc94e1ea3fad09'
    }

    # Let's register the response for api endpoint
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
def test_search(api):
    '''
    Test case for tags search method
    '''
    # Let's create sample response for api endpoint
    test_response: dict = {
        'values': [
            {
                'id': 'd3786a2c-1c0c-4b5d-8b38-c9fbf7db9a04',
                'created_at': '2021-10-19T12:06:17.529Z',
                'created_by': 'user@tenable.com',
                'updated_at': '2021-10-19T12:06:17.529Z',
                'updated_by': 'user@tenable.com',
                'category_id': '36c260ae-e3ad-4e59-afba-e65d9d436d3d',
                'value': 'Q7',
                'type': 'static',
                'category_name': 'Audi'
            },
            {
                'id': '27d6612c-3356-4023-9815-cbf5dc298403',
                'created_at': '2021-10-22T10:13:34.111Z',
                'created_by': 'szaros+us-2a@tenable.com',
                'updated_at': '2021-10-22T10:13:34.111Z',
                'updated_by': 'szaros+us-2a@tenable.com',
                'category_id': '4f3bd5fb-9f99-49c7-8deb-89f7596674d0',
                'value': 'First Value',
                'description': '',
                'type': 'dynamic',
                'category_name': 'Demo Tag',
                'category_description': ''
            }
        ],
        'pagination': {'total': 2}
    }

    fields: list = [
        'id',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        'category_id',
        'value',
        'type',
        'category_name'
    ]

    filter = {
        'and': [
            {
                'property': 'id',
                'operator': 'eq',
                'value': [
                    'd3786a2c-1c0c-4b5d-8b38-c9fbf7db9a04',
                    '27d6612c-3356-4023-9815-cbf5dc298403'
                ]
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
        f'{BASE_URL}/values/search',
        json=test_response,
        match=[responses.matchers.json_params_matcher(payload)],
    )

    tags_search_iterator1 = api.v3.vm.tags.search(
        fields=fields,
        filter=filter,
        sort=sort,
        limit=200
    )
    assert isinstance(tags_search_iterator1, SearchIterator)
    assert len(list(tags_search_iterator1)) == test_response['pagination']['total']

    tags_search_iterator2 = api.v3.vm.tags.search(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(tags_search_iterator2, CSVChunkIterator)

    tags_search_iterator3 = api.v3.vm.tags.search(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(tags_search_iterator3, Response)


@responses.activate
def test_search_categories(api):
    '''
    Test case for tags categories search API endpoint
    '''
    # Let's create sample response for api endpoint
    test_response: dict = {
        'categories': [
            {
                'id': '36c260ae-e3ad-4e59-afba-e65d9d436d3d',
                'created_at': '2021-10-19T12:06:17.518Z',
                'created_by': 'user@tenable.com',
                'updated_at': '2021-10-19T12:06:17.529Z',
                'updated_by': 'user@tenable.com',
                'name': 'Audi',
                'value_count': 1
            }
        ],
        'pagination': {
            'total': 1,
        }
    }

    fields: list = [
        'id',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        'name',
        'value_count'
    ]

    filter = {
        'and': [
            {
                'property': 'id',
                'operator': 'eq',
                'value': [
                    'd3786a2c-1c0c-4b5d-8b38-c9fbf7db9a04'
                ]
            }
        ]
    }

    sort = [('id', 'asc')]

    # Let's create sample payload for search categories endpoint
    payload = {
        'fields': fields,
        'filter': filter,
        'limit': 200,
        'sort': [{'order': 'asc', 'property': 'id'}],
    }

    # Let's register the mock response for search categories endpoint
    responses.add(
        responses.POST,
        f'{BASE_URL}/categories/search',
        json=test_response,
        match=[responses.matchers.json_params_matcher(payload)],
    )

    search_categories_iterator1 = api.v3.vm.tags.search_categories(
        fields=fields,
        filter=filter,
        sort=sort,
        limit=200
    )
    assert isinstance(search_categories_iterator1, SearchIterator)
    assert len(list(search_categories_iterator1)) == test_response['pagination']['total']

    search_categories_iterator2 = api.v3.vm.tags.search_categories(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(search_categories_iterator2, CSVChunkIterator)

    search_categories_iterator3 = api.v3.vm.tags.search_categories(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(search_categories_iterator3, Response)
