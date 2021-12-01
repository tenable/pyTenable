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
RANDOM_KEY = ''.join(random.choice('0123456789abcdefg') for i in range(64))
SCANNERS_LIST = [
    {
        'creation_date': 1635431656,
        'group': True,
        'key': RANDOM_KEY,
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
        'key': 'a02hc58d8gfcf1dh44568eh95he9hd5eb3904db5955a7ge10g0h1e793e2100ba',  # noqa: E501
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
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}',
        json={'scanners': SCANNERS_LIST},
    )
    linking_key = api.v3.vm.scanners.linking_key()

    assert linking_key == RANDOM_KEY


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
    schema = ScannerEditSchema()
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
    responses.add(
        responses.GET,
        f'{SCANNER_BASE_URL}',
        json={'scanners': SCANNERS_LIST}
    )
    resp = api.v3.vm.scanners.list()
    assert isinstance(resp, list)
    assert resp == SCANNERS_LIST


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
