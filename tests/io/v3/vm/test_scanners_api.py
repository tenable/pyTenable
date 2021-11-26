'''
Testing the Scanners endpoints
'''
import random
import uuid

import pytest
import responses
from responses import matchers
from tenable.io.v3.vm.schema import ScannerEditSchema

SCANNER_BASE_URL = r'https://cloud.tenable.com/api/v3/scanners'
BASE_URL = r'https://cloud.tenable.com'
SCANNER_ID = str(uuid.uuid1())


@responses.activate
def test_scanner_details(api):
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}',
        json={
            'creation_date': 1635431656,
            'group': True,
            'key': 'random_key',
            'last_connect': 'null',
            'last_modification_date': 1637162052,
            'license': 'null',
            'linked': 1,
            'name': 'Autoscaling WAS Scanners (Hyperwas only)',
            'network_name': 'Default',
            'num_scans': 0,
            'owner': {
                'id': 675765,
                'name': 'system',
                'uuid': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
            },
            'pool': True,
            'scan_count': 0,
            'shared': 1,
            'source': 'service',
            'status': 'on',
            'timestamp': 1637654052,
            'type': 'local',
            'user_permissions': 64,
            'id': SCANNER_ID,
            'supports_remote_logs': False,
            'supports_webapp': True,
        },
    )
    status = api.v3.vm.scanners.details(SCANNER_ID)
    assert isinstance(status, dict)
    assert status['id'] == SCANNER_ID


@responses.activate
def test_scanners_linking_key(api):
    '''
    Test the linking_key function
    '''
    key1 = ''.join(random.choice('0123456789abcdefgh') for i in range(64))
    scanners_list = [
        {
            'creation_date': 1635431656,
            'group': True,
            'key': key1,
            'last_connect': None,
            'last_modification_date': 1635431656,
            'license': {
                'agents': 512,
                'ips': 10000,
                'scanners': 2,
                'users': 30,
                'expiration_date': 1769403600,
                'evaluation': False,
                'scanners_used': 0,
                'agents_used': 0,
            },
            'linked': 1,
            'name': 'US Cloud Scanner',
            'network_name': 'Default',
            'num_scans': 0,
            'owner':{
                'owner': 'system',
                'name': 'system',
                'uuid': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e'
            },
            'pool': True,
            'scan_count': 0,
            'shared': 1,
            'source': 'service',
            'status': 'on',
            'timestamp': 1635431656,
            'type': 'local',
            'user_permissions': 64,
            'id': '00000000-0000-0000-0000-00000000000000000000000000001',
            'supports_remote_logs': False,
            'supports_webapp': True,
        },
        {
            'creation_date': 1635431655,
            'group': True,
            'key': 'a02hc58d8gfcf1dh44568eh95he9hd5eb3904db5955a7ge10g0h1e793e2100ba',
            'last_connect': None,
            'last_modification_date': 1635431655,
            'license': {
                'agents': 512,
                'ips': 10000,
                'scanners': 2,
                'users': 30,
                'expiration_date': 1769403600,
                'evaluation': False,
                'scanners_used': 0,
                'agents_used': 0,
            },
            'linked': 1,
            'name': 'maca_Test_boom',
            'network_name': 'Default',
            'num_scans': 0,
            'owner':{
                'owner': 'system',
                'name': 'system',
                'id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2r4e'
            },
            'pool': True,
            'scan_count': 0,
            'shared': 1,
            'source': 'service',
            'status': 'on',
            'timestamp': 1635431655,
            'type': 'local',
            'user_permissions': 64,
            'id': '2bd8dddb-397f-4ef7-9866-f9e4b8fa4d7d',
            'supports_remote_logs': False,
            'supports_webapp': True,
        },
    ]
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}',
        json={'scanners': scanners_list},
    )
    linking_key = api.v3.vm.scanners.linking_key()

    assert linking_key == key1


@pytest.mark.skip('API method NotImplemented in v3')
def test_scanners_allowed_scanners():
    '''
    Test the allowed_scanners function
    '''
    pass


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
    assert None is api.v3.vm.scanners.control_scan(SCANNER_ID, scan_uuid, action)


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
    schema = ScannerEditSchema()
    kwargs = {'force_plugin_update': True, 'force_ui_update': False}
    payload = schema.dump(schema.load(kwargs))
    responses.add(
        responses.PUT,
        f'{BASE_URL}/settings/{SCANNER_ID}',
        match=[matchers.json_params_matcher(payload)],
    )

    assert None is api.v3.vm.scanners.edit(
        SCANNER_ID, force_plugin_update=True, force_ui_update=False
    )


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
    key = ''.join(random.choice('0123456789abcdefgh') for i in range(65))
    responses.add(
        responses.GET, f'{SCANNER_BASE_URL}/{SCANNER_ID}/key', json={'key': key}
    )
    resp = api.v3.vm.scanners.get_scanner_key(SCANNER_ID)
    assert resp == key


@responses.activate
def test_scanners_get_scans(api):
    '''
    Test the get_scans function
    '''
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}/{SCANNER_ID}/scans',
        json={'scans': ['scans1', 'scans2']},
    )
    resp = api.v3.vm.scanners.get_scans(SCANNER_ID)
    assert isinstance(resp, list)
    assert resp == ['scans1', 'scans2']


@pytest.mark.skip('API method NotImplemented in v3')
def test_scanners_search():
    '''
    Test the search function
    '''
    pass


@responses.activate
def test_scanners_list(api):
    '''
    Test the list function
    '''
    scanners_list = [
        {
            'creation_date': 1636368862,
            'group': True,
            'id': 50431968,
            'key': '4806207638g58cec58dc6ab5a9h89c175979g35ebg3e52129438eb634a4h8d99',
            'last_connect': None,
            'last_modification_date': 1636377494,
            'linked': 1,
            'name': 'Test2',
            'network_name': 'Default',
            'num_scans': 0,
            'owner': {
                'id': 85678,
                'name': 'system',
                'uuid': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
            },
            'pool': True,
            'scan_count': 0,
            'shared': 1,
            'source': 'service',
            'status': 'on',
            'timestamp': 1636377494,
            'type': 'pool',
            'user_permissions': 128,
            'uuid': '7fa88c02-4c57-11ec-8f82-0a8bb8b04db8',
            'supports_remote_logs': False,
            'supports_webapp': False,
        },
        {
            'creation_date': 1635431655,
            'group': True,
            'id': 50392292,
            'key': '8daeba5c1cha80b3eg3g033e593f88dbb5de88g78621b2d3g706f1c78h1ead21',
            'last_connect': None,
            'last_modification_date': 1635431655,
            'license': {
                'agents': 512,
                'ips': 10000,
                'scanners': 2,
                'users': 30,
                'expiration_date': 1769403600,
                'evaluation': False,
                'scanners_used': 0,
                'agents_used': 0,
            },
            'linked': 1,
            'name': 'maca_Test_boom',
            'network_name': 'Default',
            'num_scans': 0,
            'owner': {
                'id': 16367,
                'name': 'system',
                'uuid': 'd9ea5dba-4c57-11ec-8639-0a8bb8b04db8',
            },
            'pool': True,
            'scan_count': 0,
            'shared': 1,
            'source': 'service',
            'status': 'on',
            'timestamp': 1635431655,
            'type': 'local',
            'user_permissions': 64,
            'uuid': '958b7d42-4c57-11ec-bfc6-0a8bb8b04db8',
            'supports_remote_logs': False,
            'supports_webapp': True,
        },
    ]
    responses.add(
        responses.GET, f'{SCANNER_BASE_URL}', json={'scanners': scanners_list}
    )
    resp = api.v3.vm.scanners.list()
    assert isinstance(resp, list)
    assert resp == scanners_list


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
    assert None is api.v3.vm.scanners.toggle_link_state(SCANNER_ID, True)


@pytest.mark.skip('API method NotImplemented in v3')
def test_scanners_get_permissions():
    '''
    Test the get_permissions function
    '''
    pass


@pytest.mark.skip('API method NotImplemented in v3')
def test_scanners_edit_permissions():
    '''
    Test the edit_permissions function
    '''
    pass
