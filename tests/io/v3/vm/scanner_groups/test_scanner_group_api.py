'''
Testing the Scanner groups endpoints
'''
import re

import responses
from responses import matchers

SCANNER_GROUPS_BASE_URL = r'https://cloud.tenable.com/api/v3/scanner-groups'
GROUP_ID = 'b5db63f1-551d-4789-aefa-9629c93ddc45'
SCANNER_ID = 'b5db63f1-551d-4789-aefa-9629c93ddc45'
SCANNER_GROUP_DETAILS = {
    'creation_date': '2019-12-31T20:50:23.635Z',
    'last_modification_date': '2019-12-31T20:50:23.635Z',
    'owner': 'system',
    'owner_id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
    'default_permissions': 16, 'user_permissions': 128,
    'shared': 1, 'scan_count': 0,
    'id': 'b5db63f1-551d-4789-aefa-9629c93ddc45',
    'type': 'load_balancing', 'name': 'test2',
    'network_name': 'Default', 'supports_webapp': False,
    'scanner_id': 'b5db63f1-551d-4789-aefa-9629c93ddc45',
    'owner_name': 'system'
}
SCANNER_CREATE_RESP = {
    'creation_date': '2019-12-31T20:50:23.635Z',
    'last_modification_date': '2019-12-31T20:50:23.635Z',
    'owner': 'system',
    'owner_id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
    'default_permissions': 16, 'scan_count': 0,
    'id': '6100e486-5df2-4849-9d1f-5b20c99abc97',
    'type': 'load_balancing', 'name': 'test1',
    'owner_name': 'system'
}
LIST_SCANNER_RESP = [
    {
        'creation_date': '2019-12-31T20:50:23.635Z',
        'group': True,
        'key': 'e3eeecca0d998c466af126549d68ef0f4e0d0ba3ab04a6e59a1d8a8a57079',
        'last_connect': None,
        'last_modification_date': '2019-12-31T20:50:23.635Z',
        'license': None,
        'linked': 1,
        'name': 'EU Frankfurt Cloud Scanners',
        'num_scans': 0,
        'owner': 'system',
        'owner_name': 'system',
        'owner_id': '09d69c34-4b27-469b-b861-04d57834bc25',
        'pool': True,
        'scan_count': 0,
        'source': 'service',
        'status': 'on',
        'timestamp': '2019-12-31T20:50:23.635Z',
        'type': 'local',
        'id': 'b5db63f1-551d-4789-aefa-9629c93ddc45'
    }
]
SCANNER_LIST_ROUTE_RESP = [
    {
        'route': 'example.com'
    },
    {
        'route': '10.1.2.3'
    },
    {
        'route': '2001:db8::/64'
    }
]


@responses.activate
def test_add_scanner(api):
    responses.add(
        responses.POST,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}/scanners/'
                   f'{SCANNER_ID}'),
    )
    assert None is api.v3.vm.scanner_groups.add_scanner(GROUP_ID, SCANNER_ID)


@responses.activate
def test_delete(api):
    responses.add(
        responses.DELETE,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}')
    )
    assert None is api.v3.vm.scanner_groups.delete(GROUP_ID)


@responses.activate
def test_create(api):
    name = 'test1'
    group_type = 'load_balancing'
    responses.add(
        responses.POST,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}'),
        json=SCANNER_CREATE_RESP
    )

    data = api.v3.vm.scanner_groups.create(name, group_type=group_type)
    assert isinstance(data, dict)
    assert data['name'] == name


@responses.activate
def test_delete_scanner(api):
    responses.add(
        responses.DELETE,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}/scanners/'
                   f'{SCANNER_ID}'),
    )
    assert None is api.v3.vm.scanner_groups.delete_scanner(
        GROUP_ID, SCANNER_ID
    )


@responses.activate
def test_details(api):
    name = 'test2'
    responses.add(
        responses.GET,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}'),
        json=SCANNER_GROUP_DETAILS
    )

    data = api.v3.vm.scanner_groups.details(GROUP_ID)
    assert isinstance(data, dict)
    assert data['name'] == name


@responses.activate
def test_edit(api):
    name = 'test3'
    responses.add(
        responses.PUT,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}'),
        match=[matchers.json_params_matcher({'name': name})],
    )

    data = api.v3.vm.scanner_groups.edit(GROUP_ID, name)
    assert None is data


@responses.activate
def test_list_scanners(api):
    name = 'EU Frankfurt Cloud Scanners'
    responses.add(
        responses.GET,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}/scanners'),
        json={
            'scanners': LIST_SCANNER_RESP
        }
    )

    data = api.v3.vm.scanner_groups.list_scanners(GROUP_ID)
    assert isinstance(data, list)
    assert data[0]['name'] == name


@responses.activate
def test_list_routes(api):
    responses.add(
        responses.GET,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}/routes'),
        json=SCANNER_LIST_ROUTE_RESP
    )

    data = api.v3.vm.scanner_groups.list_routes(GROUP_ID)
    assert isinstance(data, list)
    assert data[0]['route'] == 'example.com'


@responses.activate
def test_edit_routes(api):
    routes = ['127.0.0.1']
    responses.add(
        responses.PUT,
        re.compile(f'{SCANNER_GROUPS_BASE_URL}/{GROUP_ID}'),
        match=[matchers.json_params_matcher({'routes': routes})],
    )

    data = api.v3.vm.scanner_groups.edit_routes(GROUP_ID, routes)
    assert None is data
