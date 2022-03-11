'''
Testing the Scanners endpoints
'''
import random
import uuid

import pytest
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.scanners.schema import ScannerSchema

PERMISSIONS_BASE_URL = r'https://cloud.tenable.com/api/v3/permissions'
OBJECT_ID = str(uuid.uuid1())
SCANNER_BASE_URL = r'https://cloud.tenable.com/api/v3/scanners'
BASE_URL = r'https://cloud.tenable.com'
SCANNER_ID = str(uuid.uuid1())
RANDOM_KEY = ''.join(random.choice('0123456789abcdefg') for i in range(64))
SCANNERS_LIST = [
    {
        'creation_date': '2020-01-06T00:51:37.436Z',
        'group': True,
        'key': RANDOM_KEY,
        'last_connect': None,
        'last_modification_date': '2022-01-06T00:51:37.436Z',
        'license': {
            'agents': 512,
            'ips': 10000,
            'scanners': 2,
            'users': 30,
            'expiration_date': '2025-01-06T00:51:37.436Z',
            'evaluation': False,
            'scanners_used': 0,
            'agents_used': 0,
        },
        'linked': 1,
        'name': 'US Cloud Scanner',
        'network_name': 'Default',
        'num_scans': 0,
        'owner': {
            'owner': 'system',
            'name': 'system',
            'uuid': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e'
        },
        'pool': True,
        'scan_count': 0,
        'shared': 1,
        'source': 'service',
        'status': 'on',
        'timestamp': '2022-01-06T00:51:37.436Z',
        'type': 'local',
        'user_permissions': 64,
        'id': '00000000-0000-0000-0000-00000000000000000000000000001',
        'supports_remote_logs': False,
        'supports_webapp': True,
    },
    {
        'creation_date': '2021-01-06T00:51:37.436Z',
        'group': True,
        'key': 'a02hc58d8gfcf1dh44568eh95he9hd5eb3904db5955a7ge10g0h1e793e2100ba',  # noqa: E501
        'last_connect': None,
        'last_modification_date': '2022-01-06T00:51:37.436Z',
        'license': {
            'agents': 512,
            'ips': 10000,
            'scanners': 2,
            'users': 30,
            'expiration_date': '2025-01-06T00:51:37.436Z',
            'evaluation': False,
            'scanners_used': 0,
            'agents_used': 0,
        },
        'linked': 1,
        'name': 'maca_Test_boom',
        'network_name': 'Default',
        'num_scans': 0,
        'owner': {
            'owner': 'system',
            'name': 'system',
            'id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2r4e'
        },
        'pool': True,
        'scan_count': 0,
        'shared': 1,
        'source': 'service',
        'status': 'on',
        'timestamp': '2022-01-06T00:51:37.436Z',
        'type': 'local',
        'user_permissions': 64,
        'id': SCANNER_ID,
        'supports_remote_logs': False,
        'supports_webapp': True,
    },
]


@responses.activate
def test_scanner_details(api):
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}',
        json=SCANNERS_LIST[1],
    )
    status = api.v3.vm.scanners.details(SCANNER_ID)
    assert isinstance(status, dict)
    assert status['id'] == SCANNER_ID


@responses.activate
def test_scanners_linking_key(api):
    '''
    Test the linking_key function
    '''
    payload = {
        'filter': {
            'operator': 'eq',
            'property': 'id',
            'value': '00000000-0000-0000-0000-00000000000000000000000000001'
        },
        'limit': 200
    }

    api_response = {
        'scanners': [SCANNERS_LIST[0]],
        'pagination': {
            'total': 1,
            'next': 'nextToken'
        }
    }

    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}',
        json={'scanners': SCANNERS_LIST},
    )

    responses.add(
        responses.POST,
        f'{SCANNER_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )
    linking_key = api.v3.vm.scanners.linking_key()

    assert linking_key == RANDOM_KEY


def test_scanners_allowed_scanners(api):
    '''
    Test the allowed_scanners function
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.scanners.allowed_scanners()


@responses.activate
def test_scanners_control_scan(api):
    '''
    Test the control_scan function
    '''
    scan_uuid = str(uuid.uuid1())
    action = 'stop'
    responses.add(
        responses.POST,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}/scans/{scan_uuid}/control',
        match=[matchers.json_params_matcher({'action': action})],
    )
    assert api.v3.vm.scanners.control_scan(
        SCANNER_ID, scan_uuid, action) is None


@responses.activate
def test_scanners_delete(api):
    '''
    Test the delete function
    '''
    responses.add(responses.DELETE, f'{SCANNER_BASE_URL}/{SCANNER_ID}')
    assert None is api.v3.vm.scanners.delete(SCANNER_ID)


@responses.activate
def test_scanners_edit(api):
    '''
    Test the edit function
    '''
    schema = ScannerSchema()
    kwargs = {'force_plugin_update': True, 'force_ui_update': False}
    payload = schema.dump(schema.load(kwargs))
    responses.add(
        responses.PUT,
        f'{BASE_URL}/settings/{SCANNER_ID}',
        match=[matchers.json_params_matcher(payload)],
    )

    assert api.v3.vm.scanners.edit(
        SCANNER_ID, force_plugin_update=True, force_ui_update=False) is None


@responses.activate
def test_scanners_get_aws_targets(api):
    '''
    Test the get_aws_targets function
    '''
    targets = ['target1', 'target2']
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}/aws-targets',
        json={'targets': targets},
    )
    resp = api.v3.vm.scanners.get_aws_targets(SCANNER_ID)
    assert isinstance(resp, list)
    assert resp == targets


@responses.activate
def test_scanners_get_scanner_key(api):
    '''
    Test the get_scanner_key function
    '''
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}/key',
        json={'key': RANDOM_KEY}
    )
    resp = api.v3.vm.scanners.get_scanner_key(SCANNER_ID)
    assert resp == RANDOM_KEY


@responses.activate
def test_scanners_get_scans(api):
    '''
    Test the get_scans function
    '''
    scans = ['scans1', 'scans2']
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}/scans',
        json={'scans': scans},
    )
    resp = api.v3.vm.scanners.get_scans(SCANNER_ID)
    assert isinstance(resp, list)
    assert resp == scans


@responses.activate
def test_scanners_search(api):
    '''
    Test the search function
    '''
    fields = [
        'name',
        'source',
        'type',
        'id'
    ]
    sort = [('received', 'desc')]

    payload = {
        'fields': fields,
        'limit': 200,
        'sort': [{'received': 'desc'}]
    }

    api_response = {
        'scanners': [{
            'creation_date': '202-01-06T00:51:37.436Z',
            'group': True,
            'key': 'a02hc58d8gfcf1dh44568eh95he9hd5eb3904db5955a7ge10g0h1e793e2100ba',  # noqa: E501
            'last_connect': None,
            'last_modification_date': '2022-01-06T00:51:37.436Z',
            'license': {
                'agents': 512,
                'ips': 10000,
                'scanners': 2,
                'users': 30,
                'expiration_date': '2026-01-06T00:51:37.436Z',
                'evaluation': False,
                'scanners_used': 0,
                'agents_used': 0,
            },
            'linked': 1,
            'name': 'maca_Test_boom',
            'network_name': 'Default',
            'num_scans': 0,
            'owner': {
                'owner': 'system',
                'name': 'system',
                'id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2r4e'
            },
            'pool': True,
            'scan_count': 0,
            'shared': 1,
            'source': 'service',
            'status': 'on',
            'timestamp': '2022-01-06T00:51:37.436Z',
            'type': 'local',
            'user_permissions': 64,
            'id': SCANNER_ID,
            'supports_remote_logs': False,
            'supports_webapp': True,
        }],
        'pagination': {
            'total': 1,
            'next': 'nextToken'
        }
    }
    responses.add(
        responses.POST,
        f'{SCANNER_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.vm.scanners.search(
        fields=fields, limit=200, sort=sort
    )
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.vm.scanners.search(
        fields=fields, return_csv=True, sort=sort, limit=200
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.scanners.search(
        fields=fields, return_resp=True, limit=200, sort=sort
    )
    assert isinstance(resp, Response)


@responses.activate
def test_scanners_toggle_link_state(api):
    '''
    Test the toggle_link_state function
    '''
    responses.add(
        responses.PUT,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}/link',
        match=[matchers.json_params_matcher({'link': int(True)})],
    )
    assert api.v3.vm.scanners.toggle_link_state(SCANNER_ID, True) is None


@responses.activate
def test_scanners_get_permissions(api):
    '''
    Test the get_permissions function
    '''
    otype = 'scanner'
    api_resp = {
        'acls': [{
            'type': 'user',
            'id': 2236706,
            'uuid': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
            'name': 'system',
            'display_name': 'system',
            'permissions': 128,
            'owner': 1
        }, {
            'type': 'default',
            'permissions': 16
        }]
    }
    responses.add(
        responses.GET,
        f'{PERMISSIONS_BASE_URL}/{otype}/{OBJECT_ID}',
        json=api_resp
    )
    resp = api.v3.vm.scanners.get_permissions(OBJECT_ID)
    assert resp == api_resp['acls']


@responses.activate
def test_scanners_edit_permissions(api):
    '''
    Test the edit_permissions function
    '''
    otype = 'scanner'
    acls = {
        'type': 'user',
        'id': 1,
        'permissions': 128
    }
    responses.add(
        responses.PUT,
        f'{PERMISSIONS_BASE_URL}/{otype}/{OBJECT_ID}',
        match=[matchers.json_params_matcher({'acls': [acls]})]
    )
    assert api.v3.vm.scanners.edit_permissions(OBJECT_ID, acls) is None
