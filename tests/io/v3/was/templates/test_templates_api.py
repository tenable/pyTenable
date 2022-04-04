'''
Test Templates
'''
import requests
import responses

from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)

WAS_TEMPLATES_BASE_URL = 'https://cloud.tenable.com/api/v3/was/templates'
TEMPLATE_ID = '74ce1a64-acf1-4eca-955e-5668302585ba'

TEMPLATE = {
    'template_id': TEMPLATE_ID,
    'name': 'config_audit',
    'description': 'An audit of web application compliance with '
                   'configuration security guidelines.',
    'plugin_state': 'locked',
    'scanner_types': ['scanner', 'container_group', 'cloud_group'],
    'settings': {
        'timeout': '00:10:00',
        'queue_timeout': '08:00:00',
        'debug_mode': False,
        'scope': {
            'option': 'urls',
            'dom_depth_limit': 1,
            'page_limit': 1,
            'exclude_binaries': True,
            'auto_redundant_paths': 1,
            'openapi_file': None,
            'openapi_filename': None,
            'crawl_script_filename': None,
        },
        'audit': {
            'xmls': False,
            'forms': False,
            'jsons': False,
            'links': False,
            'cookies': False,
            'headers': False,
            'ui_forms': False,
            'ui_inputs': False,
            'parameter_names': False,
            'parameter_values': False,
            'path_parameters': False,
        },
        'assessment': {
            'enable': True,
            'dictionary': 'limited',
            'element_exclusions': None,
            'bruteforce': None,
        },
        'browser': {
            'screen_width': 1600,
            'screen_height': 1200,
            'ignore_images': True,
            'job_timeout': 60,
            'pool_size': 1,
        },
        'http': {
            'response_max_size': 5000000,
            'request_redirect_limit': 2,
            'user_agent': 'WAS/%v',
            'custom_user_agent': False,
            'request_concurrency': 10,
            'request_timeout': 30,
            'request_headers': {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            'include_scan_id': False,
        },
        'plugin': {
            'rate_limiter': {
                'requests_per_second': 25,
                'autothrottle': True,
                'timeout_threshold': 100,
            }
        },
    },
    'defaults': {
        'timeout': '00:10:00',
        'queue_timeout': '08:00:00',
        'debug_mode': False,
        'scope': {
            'option': 'urls',
            'dom_depth_limit': 1,
            'page_limit': 1,
            'exclude_binaries': True,
            'auto_redundant_paths': 1,
            'openapi_file': None,
            'openapi_filename': None,
            'crawl_script_filename': None,
        },
        'audit': {
            'xmls': False,
            'forms': False,
            'jsons': False,
            'links': False,
            'cookies': False,
            'headers': False,
            'ui_forms': False,
            'ui_inputs': False,
            'parameter_names': False,
            'parameter_values': False,
            'path_parameters': False,
        },
        'assessment': {
            'enable': True,
            'dictionary': 'limited',
            'element_exclusions': None,
            'bruteforce': None,
        },
        'browser': {
            'screen_width': 1600,
            'screen_height': 1200,
            'ignore_images': True,
            'job_timeout': 60,
            'pool_size': 1,
        },
        'http': {
            'response_max_size': 5000000,
            'request_redirect_limit': 2,
            'user_agent': 'WAS/%v',
            'custom_user_agent': False,
            'request_concurrency': 10,
            'request_timeout': 30,
            'request_headers': {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            'include_scan_id': False,
        },
        'plugin': {
            'rate_limiter': {
                'requests_per_second': 25,
                'autothrottle': True,
                'timeout_threshold': 100,
            }
        },
    },
    'plugins': [
        {
            'plugin_id': 112535,
            'name': 'HTTP Strict Transport Security Policy Detected',
            'family': 'HTTP Security Header',
            'policy': ['api', 'config_audit', 'overview', 'pci', 'scan'],
        },
        {
            'plugin_id': 112526,
            'name': 'Missing "X-XSS-Protection" Header',
            'family': 'HTTP Security Header',
            'policy': ['pci', 'scan', 'overview', 'config_audit'],
        }
    ],
}


@responses.activate
def test_details(api):
    '''
    Test was folders details method
    '''
    responses.add(
        responses.GET,
        f'{WAS_TEMPLATES_BASE_URL}/{TEMPLATE_ID}',
        json=TEMPLATE,
    )
    template = api.v3.was.templates.details(TEMPLATE_ID)
    assert template == TEMPLATE
    assert template['template_id'] == TEMPLATE_ID


@responses.activate
def test_search(api):
    '''
    Test was templates search method
    '''
    response = {
        'items': [TEMPLATE],
        'pagination': {
            'total': 1
        }
    }

    fields = ['template_id', 'name', 'description', 'plugin_state',
              'scanner_types', 'settings', 'defaults', 'plugins']

    filters = {'operator': 'eq', 'property': 'plugin_state', 'value': 'locked'}

    sort = [('name', 'asc')]

    api_payload = {
        'fields': fields,
        'filter': filters
    }

    responses.add(
        responses.POST,
        f'{WAS_TEMPLATES_BASE_URL}/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )

    resp = api.v3.was.templates.search(fields=fields,
                                       filter=filters,
                                       sort=sort,
                                       limit=2)
    assert isinstance(resp, SearchIterator)

    for account in resp:
        assert account == TEMPLATE

    resp = api.v3.was.templates.search(fields=fields,
                                       filter=filters,
                                       sort=sort,
                                       limit=2,
                                       return_csv=True
                                       )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.was.templates.search(fields=fields,
                                       filter=filters,
                                       sort=sort,
                                       limit=2,
                                       return_resp=True
                                       )
    assert isinstance(resp, requests.Response)
