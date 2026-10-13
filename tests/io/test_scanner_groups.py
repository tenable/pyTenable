"""
test scanner_groups
"""

import uuid

import pytest
import responses

from tenable.errors import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    ServerError,
    UnexpectedValueError,
)
from tests.checker import check


@responses.activate
def test_add_scanner_to_scanner_group_notfounderror(tvm):
    """
    test to raise exception when scanner_id or group_id not found.
    """
    responses.add(
        responses.POST,
        'https://nourl/scanner-groups/1/scanners/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'ScannerGroup with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanner_groups.add_scanner(1, 1)


@responses.activate
def test_add_scanner_to_scanner_group_permissionerror(tvm):
    """
    test to raise exception when standard user try to add scanner to group.
    """
    responses.add(
        responses.POST,
        'https://nourl/scanner-groups/1/scanners/1',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.add_scanner(1, 1)


@responses.activate
def test_add_scanner_to_group(tvm, scanner, scannergroup):
    """
    test to add scanner to scanner_group
    """
    responses.add(responses.POST, 'https://nourl/scanner-groups/102797/scanners/131712')
    tvm.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])


def test_create_scanner_group_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scanner_groups.create(1)


def test_create_scanner_group_type_typeerror(tvm):
    """
    test to raise exception when type of group_type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scanner_groups.create(str(uuid.uuid4()), group_type=1)


def test_create_scanner_group_type_unexpectedvalue(tvm):
    """
    test to raise exception when group_type param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.scanner_groups.create(str(uuid.uuid4()), group_type='normal')


@responses.activate
def test_create_scanner_group_permissionerror(tvm):
    """
    test to raise exception when standard user try to create scanner group.
    """
    responses.add(
        responses.POST,
        'https://nourl/scanner-groups',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.create(str(uuid.uuid4()))


@responses.activate
def test_create_scanner_group(tvm, scannergroup):
    """
    test to create scanner_group
    """
    responses.add(responses.POST, 'https://nourl/scanner-groups', json=scannergroup)
    scannergroup = tvm.scanner_groups.create(scannergroup['name'])
    assert isinstance(scannergroup, dict)
    scanner_group = scannergroup
    check(scanner_group, 'default_permissions', int)
    check(scanner_group, 'id', int)
    check(scanner_group, 'last_modification_date', int)
    check(scanner_group, 'name', str)
    check(scanner_group, 'owner', str)
    check(scanner_group, 'owner_id', int)
    check(scanner_group, 'owner_name', str)
    check(scanner_group, 'owner_uuid', 'uuid')
    check(scanner_group, 'scan_count', int)
    check(scanner_group, 'type', str)
    check(scanner_group, 'uuid', 'uuid')


@responses.activate
def test_delete_scanner_group_notfound(tvm):
    """
    test to raise exception when user provided group_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanner-groups/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'ScannerGroup with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanner_groups.delete(1)


@responses.activate
def test_delete_scanner_group_permissionserror(tvm):
    """
    test to raise exception when standard user try to delete scanner group.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanner-groups/1',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.delete(1)


@responses.activate
def test_delete_scanner_group(tvm, scannergroup):
    """
    test to delete scanner_group
    """
    responses.add(responses.DELETE, 'https://nourl/scanner-groups/102797')
    tvm.scanner_groups.delete(scannergroup['id'])


@responses.activate
def test_remove_scanner_from_scanner_group_notfounderror(tvm):
    """
    test to raise exception when scanner_id or group_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanner-groups/1/scanners/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'ScannerGroup with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanner_groups.delete_scanner(1, 1)


@responses.activate
def test_remove_scanner_from_scanner_group_permissionserror(tvm):
    """
    test to raise exception when standard user try to remove scanner from scanner group.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanner-groups/1/scanners/1',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.delete_scanner(1, 1)


@responses.activate
def test_remove_scanner_from_scanner_group(tvm, scanner, scannergroup):
    """
    test to remove scanner from scanner group
    """
    responses.add(responses.POST, 'https://nourl/scanner-groups/102797/scanners/131712')
    responses.add(
        responses.DELETE, 'https://nourl/scanner-groups/102797/scanners/131712'
    )
    tvm.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])
    tvm.scanner_groups.delete_scanner(scannergroup['id'], scanner['id'])


@pytest.mark.xfail(raises=ServerError)
@responses.activate
def test_scannergroup_details_notfounderror(tvm):
    """
    test to raise exception when group_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups/1',
        json={
            'statusCode': 500,
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred. Please wait a moment and try your request again.',
        },
        status=500,
    )
    with pytest.raises(NotFoundError):
        tvm.scanner_groups.details(1)


@responses.activate
def test_scannergroup_details_permissionerror(tvm):
    """
    test to raise exception when standard user try to get details of scanner group.
    """
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups/1',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.details(1)


@responses.activate
def test_scannergroup_details(tvm, scannergroup):
    """
    test to get details of scanner group.
    """
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups/102797',
        json={
            'creation_date': 1544138442,
            'last_modification_date': 1544138442,
            'owner_id': 1,
            'owner': 'system',
            'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
            'default_permissions': 16,
            'user_permissions': 128,
            'shared': 1,
            'scan_count': 0,
            'uuid': '714a5127-dfb4-4a18-bd2b-ae252501675e',
            'type': 'load_balancing',
            'name': 'f847b33d-1fb6-4cf5-8c89-4b2645303fbd',
            'id': 102797,
            'scanner_id': 142629,
            'scanner_uuid': '714a5127-dfb4-4a18-bd2b-ae252501675e',
            'owner_name': 'system',
        },
    )
    scanner_group = tvm.scanner_groups.details(scannergroup['id'])
    assert scanner_group['id'] == scannergroup['id']
    scanner_group = scannergroup
    check(scanner_group, 'default_permissions', int)
    check(scanner_group, 'id', int)
    check(scanner_group, 'last_modification_date', int)
    check(scanner_group, 'name', str)
    check(scanner_group, 'owner', str)
    check(scanner_group, 'owner_id', int)
    check(scanner_group, 'owner_name', str)
    check(scanner_group, 'owner_uuid', 'uuid')
    check(scanner_group, 'scan_count', int)
    check(scanner_group, 'type', str)
    check(scanner_group, 'uuid', 'uuid')


@pytest.mark.xfail(raises=ServerError)
@responses.activate
def test_edit_scanner_group_notfounderror(tvm):
    """
    test to raise exception when group_id not found.
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanner-groups/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'ScannerGroup with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanner_groups.edit(1, str(uuid.uuid4()))


@responses.activate
def test_edit_scanner_group_permissionerror(tvm):
    """
    test to raise exception when standard user try to edit name of scanner group.
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanner-groups/1',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.edit(1, str(uuid.uuid4()))


@responses.activate
def test_edit_scanner_group(tvm, scannergroup):
    """
    test to edit scanner group
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanner-groups/102797',
        json={
            'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
            'created': 1544138444633,
            'modified': 1544138445109,
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'uuid': '714a5127-dfb4-4a18-bd2b-ae252501675e',
            'id': 102797,
            'name': '9775dbb8-aa71-4f91-982b-d8e974c05744',
            'type': 'load_balancing',
            'distributed': False,
            'default_permissions': 16,
            'environment_name': 'Default',
            'shared': 1,
            'user_permissions': 128,
            'created_in_seconds': 1544138444,
            'modified_in_seconds': 1544138445,
        },
    )
    tvm.scanner_groups.edit(scannergroup['id'], str(uuid.uuid4()))


@responses.activate
def test_list_scanner_groups(tvm):
    """
    test to list scanner group
    """
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups',
        json={
            'scanner_pools': [
                {
                    'creation_date': 1540313110,
                    'last_modification_date': 1540313110,
                    'owner_id': 1,
                    'owner': 'system',
                    'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
                    'default_permissions': 16,
                    'user_permissions': 128,
                    'shared': 1,
                    'scan_count': 0,
                    'scanner_count': 0,
                    'uuid': '7699e6b9-7f14-40fe-8743-3e8d4590ed8b',
                    'type': 'load_balancing',
                    'name': 'b8e19918-1d5d-45ae-9a1d-411dd1e37036',
                    'id': 101985,
                    'scanner_id': 133509,
                    'scanner_uuid': '7699e6b9-7f14-40fe-8743-3e8d4590ed8b',
                    'owner_name': 'system',
                }
            ]
        },
    )
    groups = tvm.scanner_groups.list()
    assert isinstance(groups, list)
    for group in groups:
        check(group, 'creation_date', int)
        check(group, 'default_permissions', int)
        check(group, 'id', int)
        check(group, 'last_modification_date', int)
        check(group, 'name', str)
        check(group, 'owner', str)
        check(group, 'owner_id', int)
        check(group, 'owner_name', str)
        check(group, 'owner_uuid', 'uuid')
        check(group, 'scan_count', int)
        check(group, 'scanner_count', int)
        check(group, 'scanner_id', int)
        check(group, 'scanner_uuid', 'uuid')
        check(group, 'shared', int)
        check(group, 'type', str)
        check(group, 'user_permissions', int)
        check(group, 'uuid', 'uuid')


@responses.activate
def test_list_scanner_groups_permissionerror(tvm):
    """
    test to raise exception when standard user try to get list of scanner groups.
    """
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.list()


@responses.activate
def test_list_scanners_in_scanner_group_permissionerror(tvm, scannergroup):
    """
    test to raise exception when standard user try to get list of scanners in scanner groups.
    """
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups/102797/scanners',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanner_groups.list_scanners(scannergroup['id'])


@responses.activate
def test_list_scanners_in_scanner_group(tvm, scannergroup, scanner):
    """
    test to get list of scanners in scanner group
    """
    responses.add(responses.POST, 'https://nourl/scanner-groups/102797/scanners/131712')
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups/102797/scanners',
        json={
            'scanners': [
                {
                    'creation_date': 1538594853,
                    'distro': 'ubuntu1110-x86-64',
                    'engine_version': '8.1.0',
                    'group': False,
                    'id': 131712,
                    'key': '00304ce24d16da1ea4e6181e432010eaca13f3394b94c330965b0c0992ad133d',
                    'last_connect': 1544138419,
                    'last_modification_date': 1544128451,
                    'linked': 1,
                    'loaded_plugin_set': '201812051251',
                    'name': 'pytenable-scanner',
                    'num_hosts': 0,
                    'num_scans': 0,
                    'num_sessions': 0,
                    'num_tcp_sessions': 0,
                    'owner': 'system',
                    'owner_id': 1,
                    'owner_name': 'system',
                    'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
                    'platform': 'LINUX',
                    'pool': False,
                    'scan_count': 0,
                    'source': 'service',
                    'status': 'on',
                    'timestamp': 1544128451,
                    'type': 'managed',
                    'ui_build': '158',
                    'ui_version': '8.1.0',
                    'uuid': '3e839499-e7a5-4aa5-8a2d-61e621ea343b',
                    'remote_uuid': 'bdc6b14f-db20-dacb-04e0-960df14350c7834261cf33a01688',
                }
            ]
        },
    )
    responses.add(
        responses.DELETE, 'https://nourl/scanner-groups/102797/scanners/131712'
    )
    tvm.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])
    scanners = tvm.scanner_groups.list_scanners(scannergroup['id'])
    assert isinstance(scanners, list)
    for scanner_detail in scanners:
        check(scanner_detail, 'distro', str, allow_none=True)
        check(scanner_detail, 'engine_version', str)
        check(scanner_detail, 'group', bool)
        check(scanner_detail, 'id', int)
        check(scanner_detail, 'key', str)
        check(scanner_detail, 'last_connect', int)
        check(scanner_detail, 'last_modification_date', int)
        check(scanner_detail, 'linked', int)
        check(scanner_detail, 'loaded_plugin_set', str)
        check(scanner_detail, 'name', str)
        check(scanner_detail, 'num_hosts', int)
        check(scanner_detail, 'num_scans', int)
        check(scanner_detail, 'num_sessions', int)
        check(scanner_detail, 'num_tcp_sessions', int)
        check(scanner_detail, 'owner', str)
        check(scanner_detail, 'owner_id', int)
        check(scanner_detail, 'owner_name', str)
        check(scanner_detail, 'owner_uuid', 'uuid')
        check(scanner_detail, 'platform', str)
        check(scanner_detail, 'pool', bool)
        check(scanner_detail, 'scan_count', int)
        check(scanner_detail, 'source', str)
        check(scanner_detail, 'status', str)
        check(scanner_detail, 'timestamp', int)
        check(scanner_detail, 'type', str)
        check(scanner_detail, 'ui_build', str)
        check(scanner_detail, 'ui_version', str)
        check(scanner_detail, 'uuid', 'uuid')
    tvm.scanner_groups.delete_scanner(scannergroup['id'], scanner['id'])


@responses.activate
def test_edit_routes_in_scanner_group_invalidinputerror(tvm, scannergroup):
    """
    test to raise exception when values in routes are invalid
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanner-groups/102797/routes',
        json={'error': '127.0.0.256: Unrecognized target format'},
        status=400,
    )
    with pytest.raises(BadRequestError):
        tvm.scanner_groups.edit_routes(scannergroup['id'], ['127.0.0.256'])


def test_edit_routes_in_scanner_group_typeerror(tvm, scannergroup):
    """
    test to raise exception when type of routes param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scanner_groups.edit_routes(scannergroup['id'], '127.0.0.1')


@responses.activate
def test_edit_routes_in_scanner_group_success(tvm, scannergroup):
    """
    test to edit routes in scanner group
    """
    responses.add(responses.PUT, 'https://nourl/scanner-groups/102797/routes')
    tvm.scanner_groups.edit_routes(scannergroup['id'], ['127.0.0.1'])


@responses.activate
def test_list_routes_in_scanner_group_success(tvm, scannergroup):
    """
    test to list routes in scanner group
    """
    responses.add(responses.PUT, 'https://nourl/scanner-groups/102797/routes')
    responses.add(
        responses.GET,
        'https://nourl/scanner-groups/102797/routes',
        json=[{'route': '127.0.0.1'}],
    )
    tvm.scanner_groups.edit_routes(scannergroup['id'], ['127.0.0.1'])
    routes = tvm.scanner_groups.list_routes(scannergroup['id'])
    assert routes[0]['route'] == '127.0.0.1'
