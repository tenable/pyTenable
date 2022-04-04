'''
Testing the Permissions endpoints
'''

import uuid

import responses
from responses import matchers

PERMISSIONS_BASE_URL = r'https://cloud.tenable.com/api/v3/permissions'
BASE_URL = r'https://cloud.tenable.com'
OBJECT_ID = str(uuid.uuid1())


@responses.activate
def test_change(api):
    '''
    Test case for validating change action of Permissions API
    '''
    otype = 'scanners'
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
    assert api.v3.vm.permissions.change(otype, OBJECT_ID, acls) is None


@responses.activate
def test_list_permissions(api):
    '''
    Test case for validating list action of Permissions API
    '''
    otype = 'scanners'
    api_resp = {
        "acls": [{
            "type": "user",
            "id": "1035e55d-a984-4b1c-acc7-fd2d472126f1",
            "name": "system",
            "display_name": "system",
            "permissions": 128,
            "owner": 1
        }]
    }
    responses.add(
        responses.GET,
        f'{PERMISSIONS_BASE_URL}/{otype}/{OBJECT_ID}',
        json=api_resp
    )
    resp = api.v3.vm.permissions.list(otype, OBJECT_ID)
    assert resp == api_resp['acls']
