'''
Testing the Configurations endpoints
'''
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)

CONFIGURATIONS_BASE_URL = r'https://cloud.tenable.com/api/v3/was/configs'

CONFIGURATION_DETAILS = {
    'target': 'https://google-gruyere.appspot.com/',
    'config_id': '001c5298-78e0-3c61-8911-7681a2385076',
    'container_id': 'f00eb050-a179-4980-94f8-3b3e04e2d7ee',
    'owner_id': '5e1eab62-5176-4fa6-b92f-63a4239f1c6c',
    'template_id': 'b223f18e-5a94-4e02-b560-77a4a8246cd3',
    'user_template_id': None,
    'name': 'Gruyere Public',
    'targets': [
        'https://google-gruyere.appspot.com/'
    ],
    'description': '',
    'created_at': '2017-07-18T15:04:31Z',
    'updated_at': '2017-07-18T15:04:31Z',
    'settings': {
        'timeout': '00:05:00',
        'queue_timeout': '08:00:00',
        'debug_mode': False,
        'credentials': {
            'credential_ids': [
                '00000000-0000-0000-0000-000000000000'
            ]
        },
        'scope': {
            'option': 'all',
            'urls': None,
            'exclude_file_extensions': [
                'js',
                'css',
                'png',
                'jpeg',
                'gif',
                'pdf',
                'csv',
                'svn-base',
                'svg',
                'jpg',
                'ico'
            ],
            'exclude_path_patterns': [
                'logout'
            ],
            'dom_depth_limit': 5,
            'directory_depth_limit': 10,
            'page_limit': 10000,
            'crawl_script': None,
            'decompose_paths': False,
            'exclude_binaries': None,
            'auto_redundant_paths': None,
            'openapi_file': None,
            'openapi_filename': None,
            'crawl_script_filename': None
        },
        'plugin': {
            'rate_limiter': {
                'requests_per_second': 25,
                'autothrottle': True,
                'timeout_threshold': 100
            },
            'mode': 'disable',
            'ids': [],
            'names': [],
            'families': []
        },
        'browser': {
            'screen_width': 1600,
            'screen_height': 1200,
            'ignore_images': True,
            'job_timeout': 10,
            'analysis': None,
            'pool_size': None
        },
        'chrome': {
            'script_finish_wait': 5000,
            'script_page_load_wait': 10000,
            'script_command_wait': 500
        },
        'assessment': {
            'enable': True,
            'dictionary': 'limited',
            'rfi_remote_url': None,
            'fingerprinting': None,
            'element_exclusions': None,
            'bruteforce': None
        },
        'audit': {
            'forms': True,
            'cookies': True,
            'ui_forms': True,
            'ui_inputs': True,
            'headers': True,
            'links': True,
            'parameter_names': False,
            'parameter_values': True,
            'jsons': False,
            'xmls': False,
            'path_parameters': False
        }
    },
    'scanner_id': 1,
    'schedule': {
        'rrule': 'FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1',
        'starttime': '2021-11-09T08:41:09+00:00',
        'timezone': 'America/New_York',
        'enabled': False
    },
    'folder': {
        'folder_id': '5d4498a7-e066-4711-86c7-6ca136df9b32',
        'name': 'Test Folder'
    },
    'in_trash': False,
    'additional_properties': None,
    'default_permissions': 'no_access',
    'results_visibility': 'dashboard',
    'permissions': [
        {
            'entity': 'user',
            'entity_id': '3f79d8d6-abc9-493c-b019-086d9de549c9',
            'level': 'configure',
            'permissions_id': '8fbef377-b252-411d-95c8-bc3deac425ed'
        }
    ],
    'notifications': {
        'emails': []
    }
}

CONFIGURATION_ID = '001c5298-78e0-3c61-8911-7681a2385076'


@responses.activate
def test_create(api):
    '''
    Test Create Configurations.
    '''

    create_config_payload = dict()

    create_config_payload['name'] = CONFIGURATION_DETAILS['name']
    create_config_payload['owner_id'] = CONFIGURATION_DETAILS['owner_id']
    create_config_payload['template_id'] = CONFIGURATION_DETAILS['template_id']
    create_config_payload['targets'] = CONFIGURATION_DETAILS['targets']
    create_config_payload['settings'] = CONFIGURATION_DETAILS['settings']
    create_config_payload['permissions'] = CONFIGURATION_DETAILS['permissions']
    create_config_payload['schedule'] = CONFIGURATION_DETAILS['schedule']

    responses.add(
        responses.POST,
        CONFIGURATIONS_BASE_URL,
        match=[matchers.json_params_matcher(create_config_payload)],
        json=CONFIGURATION_DETAILS
    )

    resp = api.v3.was.configurations.create(
        CONFIGURATION_DETAILS['name'],
        CONFIGURATION_DETAILS['owner_id'],
        CONFIGURATION_DETAILS['template_id'],
        CONFIGURATION_DETAILS['targets'],
        CONFIGURATION_DETAILS['settings'],
        permissions=CONFIGURATION_DETAILS['permissions'],
        schedule=CONFIGURATION_DETAILS['schedule']
    )

    assert resp['config_id'] == '001c5298-78e0-3c61-8911-7681a2385076'
    assert resp['additional_properties'] is None
    assert resp['permissions'][0]['permissions_id'] == '8fbef377-b252-411d-95c8-bc3deac425ed'  # noqa: E501


@responses.activate
def test_delete(api):
    '''
    Test Delete Configurations.
    '''
    responses.add(
        responses.DELETE,
        f'{CONFIGURATIONS_BASE_URL}/{CONFIGURATION_ID}',
        status=202
    )
    resp = api.v3.was.configurations.delete(CONFIGURATION_ID)
    assert resp.status_code == 202


@responses.activate
def test_details(api):
    '''
    Test Details Configurations.
    '''
    responses.add(
        responses.GET,
        f'{CONFIGURATIONS_BASE_URL}/{CONFIGURATION_ID}',
        json=CONFIGURATION_DETAILS
    )
    resp = api.v3.was.configurations.details(CONFIGURATION_ID)

    assert resp['owner_id'] == '5e1eab62-5176-4fa6-b92f-63a4239f1c6c'
    assert resp['name'] == 'Gruyere Public'


@responses.activate
def test_processing_status(api):
    '''
    Test Get Configurations Processing Status.
    '''

    tracking_id = 'bacfce5b-71c2-4411-825a-39eb192ccf50'
    responses.add(
        responses.GET,
        f'{CONFIGURATIONS_BASE_URL}/{CONFIGURATION_ID}/status/{tracking_id}',
        json={
            'tracking_status': 'completed'
        }
    )
    resp = api.v3.was.configurations.get_processing_status(CONFIGURATION_ID,
                                                           tracking_id)

    assert resp['tracking_status'] == 'completed'


@responses.activate
def test_move(api):
    '''
    Test Move Configurations.
    '''
    responses.add(
        responses.PATCH,
        f'{CONFIGURATIONS_BASE_URL}/{CONFIGURATION_ID}',
        match=[matchers.json_params_matcher({'folder_name': 'Test Folder'})],
        status=200
    )
    resp = api.v3.was.configurations.move(CONFIGURATION_ID, 'Test Folder')
    assert resp.status_code == 200


@responses.activate
def test_search(api):
    '''
    Test Search Configurations.
    '''

    fields = [
        'config_id',
        'owner_id',
        'template_id',
        'name',
        'description',
        'created_at',
    ]

    sort = [
        ('name', 'asc'),
        ('created_at', 'desc')
    ]

    filters = ('name', 'eq', 'Gruyere Public')

    payload = {
        'fields': fields,
        'filter': {
            'property': 'name',
            'operator': 'eq',
            'value': 'Gruyere Public'
        }
    }

    api_response = {
        'items': [
            {
                'config_id': '001c5298-78e0-3c61-8911-7681a2385076',
                'owner_id': '5e1eab62-5176-4fa6-b92f-63a4239f1c6c',
                'template_id': 'b223f18e-5a94-4e02-b560-77a4a8246cd3',
                'name': 'Gruyere Public',
                'description': 'Test Configuration',
                'created_at': '2017-07-18T15:04:31Z'
            }
        ],
        'pagination': {
            'total': 1
        }
    }
    responses.add(
        responses.POST,
        f'{CONFIGURATIONS_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    configurations_search_iterator1 = api.v3.was.configurations.search(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(configurations_search_iterator1, SearchIterator)

    assert len(list(configurations_search_iterator1)) == api_response['pagination']['total']

    configurations_search_iterator2 = api.v3.was.configurations.search(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(configurations_search_iterator2, CSVChunkIterator)

    configurations_search_iterator3 = api.v3.was.configurations.search(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(configurations_search_iterator3, Response)


@responses.activate
def test_upsert(api):
    '''
    Test Upsert Configurations.
    '''

    upsert_config_payload = dict()

    upsert_config_payload['name'] = CONFIGURATION_DETAILS['name']
    upsert_config_payload['owner_id'] = CONFIGURATION_DETAILS['owner_id']
    upsert_config_payload['template_id'] = CONFIGURATION_DETAILS['template_id']
    upsert_config_payload['targets'] = CONFIGURATION_DETAILS['targets']
    upsert_config_payload['settings'] = CONFIGURATION_DETAILS['settings']
    upsert_config_payload['permissions'] = CONFIGURATION_DETAILS['permissions']
    upsert_config_payload['schedule'] = CONFIGURATION_DETAILS['schedule']

    responses.add(
        responses.PUT,
        f'{CONFIGURATIONS_BASE_URL}/{CONFIGURATION_ID}',
        match=[matchers.json_params_matcher(upsert_config_payload)],
        json=CONFIGURATION_DETAILS
    )

    resp = api.v3.was.configurations.upsert(
        CONFIGURATION_ID,
        CONFIGURATION_DETAILS['name'],
        CONFIGURATION_DETAILS['owner_id'],
        CONFIGURATION_DETAILS['template_id'],
        CONFIGURATION_DETAILS['targets'],
        CONFIGURATION_DETAILS['settings'],
        permissions=CONFIGURATION_DETAILS['permissions'],
        schedule=CONFIGURATION_DETAILS['schedule']
    )

    assert resp['config_id'] == '001c5298-78e0-3c61-8911-7681a2385076'
    assert resp['additional_properties'] is None
    assert resp['permissions'][0]['permissions_id'] == '8fbef377-b252-411d-95c8-bc3deac425ed'  # noqa: E501
