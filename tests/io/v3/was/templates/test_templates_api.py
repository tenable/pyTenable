import pytest
import responses

WAS_TEMPLATES_BASE_URL = 'https://cloud.tenable.com/api/v3/was/templates'
TEMPLATE_ID = '74ce1a64-acf1-4eca-955e-5668302585ba'
TEMPLATE = {
    'id': TEMPLATE_ID,
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
        },
        {
            'plugin_id': 112527,
            'name': 'Disabled "X-XSS-Protection" Header',
            'family': 'HTTP Security Header',
            'policy': ['pci', 'config_audit', 'scan', 'overview'],
        },
        {
            'plugin_id': 98060,
            'name': 'Missing "X-Frame-Options" Header',
            'family': 'HTTP Security Header',
            'policy': ['config_audit', 'pci', 'overview', 'scan'],
        },
        {
            'plugin_id': 98648,
            'name': 'Missing "Content-Type" Header',
            'family': 'HTTP Security Header',
            'policy': ['scan', 'api', 'config_audit', 'pci', 'overview'],
        },
        {
            'plugin_id': 98715,
            'name': 'Permissive HTTP Strict Transport Security Policy'
                    'Detected',
            'family': 'HTTP Security Header',
            'policy': ['api', 'scan', 'pci', 'overview', 'config_audit'],
        },
        {
            'plugin_id': 112554,
            'name': 'Permissive Content Security Policy Detected',
            'family': 'HTTP Security Header',
            'policy': ['config_audit', 'overview', 'scan', 'pci'],
        },
        {
            'plugin_id': 112650,
            'name': 'TLS Web Server Authentication Extension Not'
                    'Supported',
            'family': 'SSL/TLS',
            'policy': ['config_audit', 'scan', 'pci', 'api', 'ssl_tls'],
        },
        {
            'plugin_id': 112537,
            'name': 'SSL/TLS None Cipher Suites Supported',
            'family': 'SSL/TLS',
            'policy': ['ssl_tls', 'config_audit', 'api', 'pci', 'scan'],
        },
        {
            'plugin_id': 98064,
            'name': 'Cookie Without Secure Flag Detected',
            'family': 'Web Applications',
            'policy': ['pci', 'overview', 'config_audit', 'scan'],
        },
        {
            'plugin_id': 113045,
            'name': 'SSL/TLS Certificate Contains Wildcard Entries',
            'family': 'SSL/TLS',
            'policy': ['config_audit', 'ssl_tls', 'scan', 'api', 'pci'],
        },
        {
            'plugin_id': 115540,
            'name': 'Cookie Without SameSite Flag Detected',
            'family': 'Web Applications',
            'policy': ['scan', 'pci', 'overview', 'config_audit'],
        },
        {
            'plugin_id': 115491,
            'name': 'SSL/TLS Cipher Suites Supported',
            'family': 'SSL/TLS',
            'policy': ['config_audit', 'ssl_tls', 'scan', 'pci', 'api'],
        },
        {
            'plugin_id': 112538,
            'name': 'SSL/TLS Insecure Cipher Suites Supported',
            'family': 'SSL/TLS',
            'policy': ['scan', 'api', 'pci', 'ssl_tls', 'config_audit'],
        },
        {
            'plugin_id': 112543,
            'name': 'HTTPS Not Detected',
            'family': 'SSL/TLS',
            'policy': ['scan', 'pci', 'ssl_tls', 'config_audit', 'api'],
        },
        {
            'plugin_id': 112495,
            'name': 'SSL/TLS Self-Signed Certificate',
            'family': 'SSL/TLS',
            'policy': ['ssl_tls', 'scan', 'pci', 'api', 'config_audit'],
        },
        {
            'plugin_id': 112551,
            'name': 'Missing Content Security Policy',
            'family': 'HTTP Security Header',
            'policy': ['pci', 'overview', 'config_audit', 'scan'],
        },
        {
            'plugin_id': 112542,
            'name': 'SSL/TLS Certificate Signed Using Weak Hashing'
                    'Algorithm',
            'family': 'SSL/TLS',
            'policy': ['ssl_tls', 'pci', 'api', 'scan', 'config_audit'],
        },
        {
            'plugin_id': 112493,
            'name': 'SSL/TLS Certificate Expired',
            'family': 'SSL/TLS',
            'policy': ['pci', 'ssl_tls', 'scan', 'api', 'config_audit'],
        },
        {
            'plugin_id': 98057,
            'name': 'Insecure "Access-Control-Allow-Origin" Header',
            'family': 'HTTP Security Header',
            'policy': ['config_audit', 'api', 'scan', 'pci', 'overview'],
        },
        {
            'plugin_id': 112494,
            'name': 'SSL Insecure Protocols',
            'family': 'SSL/TLS',
            'policy': ['config_audit', 'ssl_tls', 'api', 'pci', 'scan'],
        },
        {
            'plugin_id': 112540,
            'name': 'SSL/TLS Certificate RSA Keys Less Than 2048 bits',
            'family': 'SSL/TLS',
            'policy': ['scan', 'api', 'pci', 'config_audit', 'ssl_tls'],
        },
        {
            'plugin_id': 98062,
            'name': 'Cookie set for parent domain',
            'family': 'Web Applications',
            'policy': ['config_audit', 'overview', 'pci', 'scan'],
        },
        {
            'plugin_id': 98527,
            'name': 'Missing Referrer Policy',
            'family': 'HTTP Security Header',
            'policy': ['scan', 'overview', 'config_audit', 'pci'],
        },
        {
            'plugin_id': 112491,
            'name': 'SSL/TLS Certificate Information',
            'family': 'SSL/TLS',
            'policy': ['api', 'scan', 'config_audit', 'ssl_tls', 'pci'],
        },
        {
            'plugin_id': 98056,
            'name': 'Missing HTTP Strict Transport Security Policy',
            'family': 'HTTP Security Header',
            'policy': ['scan', 'api', 'config_audit', 'pci', 'overview'],
        },
        {
            'plugin_id': 112546,
            'name': 'TLS 1.1 Weak Protocol',
            'family': 'SSL/TLS',
            'policy': ['scan', 'ssl_tls', 'config_audit', 'pci', 'api'],
        },
        {
            'plugin_id': 98618,
            'name': 'HTTP Header Information Disclosure',
            'family': 'HTTP Security Header',
            'policy': ['overview', 'scan', 'config_audit', 'api', 'pci'],
        },
        {
            'plugin_id': 98091,
            'name': 'Mixed Resource Detection',
            'family': 'Web Applications',
            'policy': [
                'ssl_tls',
                'config_audit',
                'scan',
                'pci',
                'overview',
            ],
        },
        {
            'plugin_id': 112552,
            'name': 'Deprecated Content Security Policy',
            'family': 'HTTP Security Header',
            'policy': ['overview', 'scan', 'pci', 'config_audit'],
        },
        {
            'plugin_id': 112544,
            'name': 'HTTP to HTTPS Redirect Not Enabled',
            'family': 'SSL/TLS',
            'policy': ['pci', 'scan', 'ssl_tls', 'api', 'config_audit'],
        },
        {
            'plugin_id': 112541,
            'name': 'SSL/TLS Certificate Common Name Mismatch',
            'family': 'SSL/TLS',
            'policy': ['scan', 'ssl_tls', 'api', 'pci', 'config_audit'],
        },
        {
            'plugin_id': 112539,
            'name': 'SSL/TLS Weak Cipher Suites Supported',
            'family': 'SSL/TLS',
            'policy': ['api', 'config_audit', 'ssl_tls', 'scan', 'pci'],
        },
        {
            'plugin_id': 112598,
            'name': 'SSL/TLS Server Cipher Suite Preference',
            'family': 'SSL/TLS',
            'policy': ['pci', 'config_audit', 'api', 'ssl_tls', 'scan'],
        },
        {
            'plugin_id': 98617,
            'name': 'SSL/TLS Forward Secrecy Cipher Suites Not Supported',
            'family': 'SSL/TLS',
            'policy': ['pci', 'config_audit', 'api', 'scan', 'ssl_tls'],
        },
        {
            'plugin_id': 112599,
            'name': 'SSL/TLS Server Cipher Suite Preference Not Detected',
            'family': 'SSL/TLS',
            'policy': ['api', 'pci', 'ssl_tls', 'scan', 'config_audit'],
        },
        {
            'plugin_id': 112529,
            'name': 'Missing "X-Content-Type-Options" Header',
            'family': 'HTTP Security Header',
            'policy': ['config_audit', 'overview', 'api', 'pci', 'scan'],
        },
        {
            'plugin_id': 98063,
            'name': 'Cookie Without HttpOnly Flag Detected',
            'family': 'Web Applications',
            'policy': ['overview', 'pci', 'config_audit', 'scan'],
        },
        {
            'plugin_id': 112496,
            'name': 'TLS 1.0 Weak Protocol',
            'family': 'SSL/TLS',
            'policy': ['config_audit', 'api', 'pci', 'scan', 'ssl_tls'],
        },
        {
            'plugin_id': 112536,
            'name': 'SSL/TLS Anonymous Cipher Suites Supported',
            'family': 'SSL/TLS',
            'policy': ['api', 'scan', 'config_audit', 'pci', 'ssl_tls'],
        },
        {
            'plugin_id': 98612,
            'name': 'Missing "Expect-CT" Header',
            'family': 'HTTP Security Header',
            'policy': ['scan', 'pci', 'config_audit', 'api', 'overview'],
        },
        {
            'plugin_id': 112530,
            'name': 'SSL/TLS Versions Supported',
            'family': 'SSL/TLS',
            'policy': ['config_audit', 'api', 'pci', 'scan', 'ssl_tls'],
        },
        {
            'plugin_id': 112563,
            'name': 'SSL/TLS Certificate Lifetime Greater Than 398 Days',
            'family': 'SSL/TLS',
            'policy': ['config_audit', 'api', 'scan', 'ssl_tls', 'pci'],
        },
        {
            'plugin_id': 98616,
            'name': 'TLS 1.2 Not Supported Protocol',
            'family': 'SSL/TLS',
            'policy': ['pci', 'scan', 'api', 'ssl_tls', 'config_audit'],
        },
        {
            'plugin_id': 98526,
            'name': 'Missing Permissions Policy',
            'family': 'HTTP Security Header',
            'policy': ['scan', 'overview', 'pci', 'config_audit'],
        },
        {
            'plugin_id': 112553,
            'name': 'Missing "Cache-Control" Header',
            'family': 'HTTP Security Header',
            'policy': ['config_audit', 'overview', 'scan', 'pci', 'api'],
        },
        {
            'plugin_id': 112555,
            'name': 'Report Only Content Security Policy Detected',
            'family': 'HTTP Security Header',
            'policy': ['overview', 'scan', 'pci', 'config_audit'],
        },
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
    assert template['id'] == TEMPLATE_ID


@responses.activate
def test_search(api):
    '''
    Test was folders search method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.was.templates.search()
