'''
Testing the Networks endpoints
'''
import uuid

import pytest
import responses
from responses import matchers

NETWORK_BASE_URL = r'https://cloud.tenable.com/api/v3/networks'
BASE_URL = r'https://cloud.tenable.com'
NETWORK_ID = str(uuid.uuid1())


@responses.activate
def test_create(api):
    '''
    Test case for validating create action of Networks API
    '''
    api_resp = {
        'owner_id': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'created': '1984-06-02T19:05:00',
        'modified': '1984-06-02T19:09:00',
        'scanner_count': 0,
        'id': 'ca92cffe-8aed-4478-ac76-1acb155bac2a',
        'name': 'test_network_name',
        'description': '',
        'is_default': False,
        'created_by': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'modified_by': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'created_in_seconds': 1639119695,
        'modified_in_seconds': 1639119695
    }
    payload = {'name': 'test_network_name', 'description': ''}
    responses.add(
        responses.POST,
        f'{NETWORK_BASE_URL}',
        match=[matchers.json_params_matcher(payload)],
        json=api_resp
    )
    resp = api.v3.vm.networks.create('test_network_name')

    assert resp == api_resp


@responses.activate
def test_delete(api):
    '''
    Test case for validating delete action of Networks API
    '''
    responses.add(
        responses.DELETE,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}',
    )
    assert api.v3.vm.networks.delete(NETWORK_ID) is None


@responses.activate
def test_details(api):
    '''
    Test case for validating details action of Networks API
    '''

    api_resp = {
        'owner_id': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'created': '2004-06-02T19:05:00',
        'modified': '2004-06-02T19:05:00',
        'scanner_count': 0,
        'id': NETWORK_ID,
        'name': 'test_network_name',
        'description': '',
        'is_default': False,
        'created_by': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'modified_by': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'created_in_seconds': 1639119695,
        'modified_in_seconds': 1639119695
    }
    responses.add(
        responses.GET,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}',
        json=api_resp
    )
    resp = api.v3.vm.networks.details(NETWORK_ID)
    assert resp == api_resp


@responses.activate
def test_edit(api):
    '''
    Test case for validating edit action of Networks API
    '''
    api_resp_after_edit = {
        'owner_id': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'created': '2004-06-02T19:05:00',
        'modified': '2004-06-02T19:05:00',
        'scanner_count': 0,
        'id': NETWORK_ID,
        'name': 'test_network_name',
        'description': 'test_description',
        'is_default': False,
        'created_by': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'modified_by': 'e9f23194-adb7-4c02-8632-615c694c787e',
        'created_in_seconds': 1639119695,
        'modified_in_seconds': 1639119695
    }
    payload = {
        'name': 'test_network_name',
        'description': 'test_description'
    }
    responses.add(
        responses.PUT,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}',
        match=[matchers.json_params_matcher(payload)],
        json=api_resp_after_edit
    )
    resp = api.v3.vm.networks.edit(
        NETWORK_ID,
        'test_network_name',
        'test_description',
        assets_ttl_days=None
    )
    assert resp == api_resp_after_edit


@responses.activate
def test_assign_scanners_single(api):
    '''
    Test case for validating assign_scanners_single action of Networks API
    '''
    scanner_id = 'c017f3a8-599f-11ec-a805-0a8bb8b04db8'
    responses.add(
        responses.POST,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}/scanners/{scanner_id}',
    )
    resp = api.v3.vm.networks.assign_scanners(NETWORK_ID, scanner_id)
    assert resp is None


@responses.activate
def test_assign_scanners_multiple(api):
    '''
    Test case for validating assign_scanners_multiple action of Networks API
    '''
    scanner_id_list = [
        'c017f3a8-599f-11ec-a805-0a8bb8b04db8',
        'bf841a0c-599f-11ec-a0d1-0a8bb8b04db8']
    payload = {'scanner_uuids': scanner_id_list}
    responses.add(
        responses.POST,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}/scanners',
        match=[matchers.json_params_matcher(payload)],
    )
    resp = api.v3.vm.networks.assign_scanners(NETWORK_ID,
                                              'c017f3a8-599f-11ec-a805-0a8bb8b04db8',  # noqa: E501
                                              'bf841a0c-599f-11ec-a0d1-0a8bb8b04db8'  # noqa: E501
                                              )
    assert resp is None


@responses.activate
def test_list_scanners(api):
    '''
    Test case for validating list_scanners action of Networks API
    '''
    api_resp = {
        'scanners': [{
            'creation_date': '2004-06-02T19:05:00',
            'distro': '2.6.32-504.8.1.el6.x86_64',
            'engine_build': '201710101',
            'engine_version': 'NNM 5.4.0',
            'group': False,
            'key': 'bd98a384ff0e91c8f94fa7f786f8827c1eb7b28dffcfb9895f9d85bd',
            'last_connect': '1524524576',
            'last_modification_date': '2004-06-02T19:05:00',
            'linked': 1,
            'loaded_plugin_set': '201803271415',
            'name': 'NNM-540',
            'num_hosts': 0,
            'num_scans': 0,
            'num_sessions': 0,
            'num_tcp_sessions': 0,
            'owner': {
                'name': 'system',
                'id': 1,
                'uuid': 'ddbd3e11-3311-4682-9912-8e81805fd8a9'
            },
            'platform': 'LINUX',
            'pool': False,
            'report_frequency': 3600,
            'settings': {},
            'scan_count': 0,
            'source': 'service',
            'status': 'off',
            'timestamp': '2004-06-02T19:05:00',
            'type': 'managed_pvs',
            'id': '946df0af-0597-4d1e-993d-36a5c25b0d36',
            'remote_uuid': '4e7b9e29-b128-4ae5-9108-b936b35c6f1a9b9a533780b',
            'supports_remote_logs': False
        }]
    }
    responses.add(
        responses.GET,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}/scanners',
        json=api_resp
    )
    resp = api.v3.vm.networks.list_scanners(NETWORK_ID)
    assert resp == api_resp['scanners']


def test_search(api):
    '''
    Test case for validating search action of Networks API
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.networks.search()


@responses.activate
def test_unassigned_scanners(api):
    '''
    Test case for validating unassigned_scanners action of Networks API
    '''
    api_resp = {
        'scanners': [{
            'creation_date': '2004-06-02T19:05:00',
            'distro': '2.6.32-504.8.1.el6.x86_64',
            'engine_build': '201710101',
            'engine_version': 'NNM 5.4.0',
            'group': False,
            'key': 'bd98a384ff0e91c8f94fa7f786f8827c1eb7b28dffcfb9895f9d85b',
            'last_connect': '1524524576',
            'last_modification_date': '2004-06-02T19:05:00',
            'linked': 1,
            'loaded_plugin_set': '201803271415',
            'name': 'NNM-540',
            'num_hosts': 0,
            'num_scans': 0,
            'num_sessions': 0,
            'num_tcp_sessions': 0,
            'owner': {
                'name': 'system',
                'id': 1,
                'uuid': 'ddbd3e11-3311-4682-9912-8e81805fd8a9'
            },
            'platform': 'LINUX',
            'pool': False,
            'report_frequency': 3600,
            'settings': {},
            'scan_count': 0,
            'source': 'service',
            'status': 'off',
            'timestamp': '2004-06-02T19:05:00',
            'type': 'managed_pvs',
            'id': '946df0af-0597-4d1e-993d-36a5c25b0d36',
            'remote_uuid': '4e7b9e29-b128-4ae5-9108-b936b35c6f1a9b9a533780bd',
            'supports_remote_logs': False
        }]
    }
    responses.add(
        responses.GET,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}/assignable-scanners',
        json=api_resp
    )
    resp = api.v3.vm.networks.unassigned_scanners(NETWORK_ID)
    assert resp == api_resp['scanners']


@responses.activate
def test_network_asset_count(api):
    '''
    Test case for validating network_asset_count action of Networks API
    '''
    num_days = 20
    api_resp = {
        'numAssetsNotSeen': 200,
        'numAssetsTotal': 1000
    }
    responses.add(
        responses.GET,
        f'{NETWORK_BASE_URL}/{NETWORK_ID}/counts/assets-not-seen-in/{num_days}',  # noqa: E501
        json=api_resp
    )
    resp = api.v3.vm.networks.network_asset_count(NETWORK_ID, num_days)
    assert resp == api_resp
