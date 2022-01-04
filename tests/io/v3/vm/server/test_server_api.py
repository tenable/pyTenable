'''
Testing the Server API
'''

import responses

SERVER_BASE_URL = r'https://cloud.tenable.com/api/v3/server'
BASE_URL = r'https://cloud.tenable.com'


@responses.activate
def test_properties(api):
    properties_response = {
        'analytics': {
            'enabled': True,
            'key': '00000000-0000-0000-0000-000000000000',
            'site_id': 'abc',
        },
        'capabilities': {
            'multi_scanner': True,
            'multi_user': 'full',
            'report_email_config': True,
            'two_factor': {'smtp': False, 'twilio': True},
        },
        'container_db_version': '11.0.3',
        'enterprise': True,
        'evaluation': {'limitEnabled': True, 'targets': 25},
        'expiration': "2021-11-09T08:41:09Z",
        'expiration_time': 1500,
        'force_ui_reload': False,
        'idle_timeout': '30',
        'license': {
            'agents': 512,
            'evaluation': False,
            'expiration_date': "2021-11-09T08:41:09Z",
            'ips': 10000,
            'scanners': 2,
            'users': 30,
        },
        'limitEnabled': False,
        'loaded_plugin_set': '202112171226',
        'login_banner': None,
        'msp': True,
        'nessus_type': 'Nessus Cloud',
        'nessus_ui_build': '308',
        'nessus_ui_version': '11.0.375',
        'notifications': [],
        'plugin_set': '202112171226',
        'region': 'abc',
        'scanner_boottime': "2021-11-09T08:41:09Z",
        'server_build': 'D20144',
        'id': '1b6c59f6-0000-0000-0000-01996d3b57911c81433cc5c59a7b',
        'server_version': '6.9.1',
        'site_id': 'abc',
        'update': {'href': None, 'new_version': False, 'restart': False},
    }
    responses.add(responses.GET,
                  f'{SERVER_BASE_URL}/properties',
                  json=properties_response
                  )
    resp = api.v3.vm.server.properties()
    assert isinstance(resp, dict)
    assert resp == properties_response


@responses.activate
def test_status(api):
    status_response = {
        'code': 200,
        'status': 'ready'
    }
    responses.add(responses.GET,
                  f'{SERVER_BASE_URL}/status',
                  json=status_response
                  )
    resp = api.v3.vm.server.status()
    assert isinstance(resp, dict)
    assert resp == status_response
