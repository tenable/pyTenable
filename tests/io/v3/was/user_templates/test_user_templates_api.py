'''
Test User Templates API
'''
import requests
import responses

from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)

WAS_USER_TEMPLATES_URL = 'https://cloud.tenable.com/api/v3/was/user-templates'
USER_TEMPLATE_ID = '8e84d689-8ef6-4edf-b23d-a9d88f5aabda'
USER_TEMPLATE = {
    'name': '@#$',
    'template_name': 'config_audit',
    'results_visibility': 'dashboard',
    'description': 'Test 123',
    'owner_id': 'a8ff6f60-a7e0-43a5-a9d4-0bd079e1d9fa',
    'permissions': [],
    'container_id': 'f00eb050-a179-4980-94f8-3b3e04e2d7ee',
    'is_shared': True,
    'user_template_id': USER_TEMPLATE_ID,
    'user_permissions': 'configure',
    'default_permissions': 'configure',
    'created_at': '2021-03-16T06:12:56.107846Z',
    'updated_at': '2021-03-16T06:12:56.107847Z',
    'additional_properties': None,
    'settings': {
        'timeout': '00:10:00',
        'queue_timeout': '08:00:00',
        'debug_mode': False,
        'scope': {
            'option': 'urls',
            'urls': None,
            'exclude_file_extensions': None,
            'exclude_path_patterns': None,
            'dom_depth_limit': 1,
            'directory_depth_limit': None,
            'page_limit': 1,
            'crawl_script': None,
            'decompose_paths': None,
            'exclude_binaries': True,
            'auto_redundant_paths': 1,
            'openapi_file': None,
            'openapi_filename': None,
            'crawl_script_filename': None,
        },
        'plugin': {
            'rate_limiter': {
                'requests_per_second': 25,
                'autothrottle': True,
                'timeout_threshold': 100,
            },
            'mode': 'disable',
            'ids': [],
            'names': [],
            'families': [],
        },
        'browser': {
            'screen_width': 1600,
            'screen_height': 1200,
            'ignore_images': True,
            'job_timeout': 60,
            'analysis': None,
            'pool_size': 1,
        },
        'http': {
            'response_max_size': 5000000,
            'request_redirect_limit': 2,
            'user_agent': 'WAS/%v',
            'custom_user_agent': False,
            'request_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            'include_scan_id': False,
            'request_concurrency': 10,
            'request_timeout': 30,
        },
        'chrome': None,
        'assessment': {
            'enable': True,
            'dictionary': 'limited',
            'rfi_remote_url': None,
            'fingerprinting': None,
            'element_exclusions': None,
            'bruteforce': None,
        },
        'audit': {
            'forms': False,
            'cookies': False,
            'ui_forms': False,
            'ui_inputs': False,
            'headers': False,
            'links': False,
            'parameter_names': False,
            'parameter_values': False,
            'jsons': False,
            'xmls': False,
            'path_parameters': False,
        },
        'credentials': {'credential_ids': []},
    },
    'template_id': '3078d0c6-6e81-44de-b585-6921b69ff0ef',
}


@responses.activate
def test_delete(api):
    '''
    Test was folders delete method
    '''
    responses.add(
        responses.DELETE, f'{WAS_USER_TEMPLATES_URL}/{USER_TEMPLATE_ID}'
    )
    resp = api.v3.was.user_templates.delete(USER_TEMPLATE_ID)
    assert resp is None


@responses.activate
def test_details(api):
    '''
    Test was folders details method
    '''
    responses.add(
        responses.GET,
        f'{WAS_USER_TEMPLATES_URL}/{USER_TEMPLATE_ID}',
        json=USER_TEMPLATE,
    )
    resp = api.v3.was.user_templates.details(USER_TEMPLATE_ID)
    assert resp == USER_TEMPLATE
    assert resp['user_template_id'] == USER_TEMPLATE_ID


@responses.activate
def test_search(api):
    '''
    Test was templates search method
    '''
    response = {
        'items': [USER_TEMPLATE],
        'pagination': {
            'total': 1
        }
    }

    fields = ['template_id', 'settings', 'description',
              'additional_properties', 'updated_at', 'created_at',
              'default_permissions', 'user_permissions', 'user_template_id',
              'is_shared', 'container_id', 'permissions', 'owner_id',
              'description', 'results_visibility', 'template_name', 'name']

    filters = {'operator': 'eq', 'property': 'is_shared', 'value': True}

    sort = [('name', 'asc')]

    api_payload = {
        'fields': fields,
        'filter': filters
    }

    responses.add(
        responses.POST,
        f'{WAS_USER_TEMPLATES_URL}/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )

    resp = api.v3.was.user_templates.search(fields=fields,
                                            filter=filters,
                                            sort=sort,
                                            limit=2)
    assert isinstance(resp, SearchIterator)

    for account in resp:
        assert account == USER_TEMPLATE

    resp = api.v3.was.user_templates.search(fields=fields,
                                            filter=filters,
                                            sort=sort,
                                            limit=2,
                                            return_csv=True
                                            )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.was.user_templates.search(fields=fields,
                                            filter=filters,
                                            sort=sort,
                                            limit=2,
                                            return_resp=True
                                            )
    assert isinstance(resp, requests.Response)


@responses.activate
def test_update(api):
    '''
    Test was folders update method
    '''
    name = 'Edited template name'
    default_permissions = 'no_access'

    responses.add(
        responses.GET,
        f'{WAS_USER_TEMPLATES_URL}/{USER_TEMPLATE_ID}',
        json=USER_TEMPLATE
    )

    USER_TEMPLATE['name'] = 'name'
    USER_TEMPLATE['default_permissions'] = default_permissions

    responses.add(
        responses.PUT,
        f'{WAS_USER_TEMPLATES_URL}/{USER_TEMPLATE_ID}',
        json=USER_TEMPLATE,
    )
    resp = api.v3.was.user_templates.update(
        USER_TEMPLATE_ID,
        name=name,
        default_permissions=default_permissions
    )
    assert resp == USER_TEMPLATE
