"""
test scanners
"""

import uuid

import pytest
import responses

from tenable.errors import ForbiddenError, NotFoundError, UnexpectedValueError

from ..checker import check


def test_scanner_control_scans_action_typeerror(tvm):
    """
    test to raise the exception when the type of field action is not as defined
    """
    with pytest.raises(TypeError):
        tvm.scanners.control_scan(1, str(uuid.uuid4()), 1)


def test_scanner_control_scans_action_unexpectedvalue(tvm):
    """
    test to raise the exception when performed action on the scanner which is not found
    """
    with pytest.raises(UnexpectedValueError):
        tvm.scanners.control_scan(1, str(uuid.uuid4()), 'nope')


@responses.activate
def test_scanner_control_scans_notfounderror(tvm):
    """
    test to raise the exception when the standard user performs actions against
    scanner which is not found
    """
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/scans/c5e3e4c9-ee47-4fbc-9e1d-d6f39801f56c/control',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'Scanner with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanners.control_scan(1, 'c5e3e4c9-ee47-4fbc-9e1d-d6f39801f56c', 'stop')


@responses.activate
def test_scanner_control_scans_permissionerror(tvm):
    """
    test to raise the exception when standard user performs actions against
    given scanner
    """
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/scans/c5e3e4c9-ee47-4fbc-9e1d-d6f39801f56c/control',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.control_scan(1, 'c5e3e4c9-ee47-4fbc-9e1d-d6f39801f56c', 'stop')


@responses.activate
def test_scanner_delete_notfound(tvm):
    """
    test to raise the exception when the id is not found to delete the scanner
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanners/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'Scanner with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanners.delete(1)


@responses.activate
def test_scanner_delete_permissionerror(tvm, scanner):
    """
    test to raise the exception when the standard user gets when tried to delete the scanner
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanners/131712',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.delete(scanner['id'])


@pytest.mark.skip(reason="We don't want to actually delete scanners.")
def test_scanner_delete(tvm, scanner):
    """
    test to delete the scanners
    """
    tvm.scanners.delete(scanner['id'])


@responses.activate
def test_scanner_details_notfounderror(tvm):
    """
    test to raise the exception when the details of the scanners not found
    """
    responses.add(responses.GET, 'https://nourl/scanners/1', status=404)
    with pytest.raises(NotFoundError):
        tvm.scanners.details(1)


@responses.activate
def test_scanner_details_permissionerror(tvm, scanner):
    """
    test to raise the exception when standatd user tries to get the details
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/131712',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.details(scanner['id'])


@responses.activate
def test_scanner_details(tvm, scanner):
    """
    test to get the scanner details
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/131712',
        json={
            'creation_date': 1538594853,
            'distro': 'ubuntu1110-x86-64',
            'engine_version': '8.1.0',
            'group': False,
            'id': 131712,
            'key': '00304ce24d16da1ea4e6181e432010eaca13f3394b94c330965b0c0992ad133d',
            'last_connect': 1544138452,
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
            'shared': 1,
            'source': 'service',
            'status': 'on',
            'timestamp': 1544128451,
            'type': 'managed',
            'ui_build': '158',
            'ui_version': '8.1.0',
            'user_permissions': 128,
            'uuid': '3e839499-e7a5-4aa5-8a2d-61e621ea343b',
            'remote_uuid': 'bdc6b14f-db20-dacb-04e0-960df14350c7834261cf33a01688',
        },
    )
    each_scanner = tvm.scanners.details(scanner['id'])
    check(each_scanner, 'id', int)
    check(each_scanner, 'uuid', 'scanner-uuid')
    check(each_scanner, 'name', str)
    check(each_scanner, 'type', str)
    check(each_scanner, 'status', str)
    check(each_scanner, 'scan_count', int)
    check(each_scanner, 'engine_version', str)
    check(each_scanner, 'platform', str)
    check(each_scanner, 'loaded_plugin_set', str)
    check(each_scanner, 'owner', str)
    check(each_scanner, 'pool', bool)


def test_sanner_edit_plugin_update_typeerror(tvm, scanner):
    """
    test to raise the exception when the type of field force_plugin_update is not as defined
    """
    with pytest.raises(TypeError):
        tvm.scanners.edit(scanner['id'], force_plugin_update='yup')


def test_scanner_edit_ui_update_typeerror(tvm, scanner):
    """
    test to raise the exception when the type of field force_ui_update is not as defined
    """
    with pytest.raises(TypeError):
        tvm.scanners.edit(scanner['id'], force_ui_update='yup')


def test_scanner_edit_finish_update_typeerror(tvm, scanner):
    """
    test to raise the exception when the type of field finish_update is not as defined
    """
    with pytest.raises(TypeError):
        tvm.scanners.edit(scanner['id'], finish_update='yup')


def test_scanner_edit_registration_code_typeerror(tvm, scanner):
    """
    test to raise the exception when the type of field registration_code is not as defined
    """
    with pytest.raises(TypeError):
        tvm.scanners.edit(scanner['id'], registration_code=False)


def test_scanner_edit_aws_update_typeerror(tvm, scanner):
    """
    test to raise the exception when the type of field aws update interval is not as defined
    """
    with pytest.raises(TypeError):
        tvm.scanners.edit(scanner['id'], aws_update_interval='nope')


@pytest.mark.xfail(raises=ForbiddenError)
@responses.activate
def test_scanner_edit_notfounderror(tvm):
    """
    test to raise the exception when tried to edit the scanner which is not found
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'Scanner with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanners.edit(1, force_ui_update=True)


@responses.activate
def test_scanner_edit_permissionserror(tvm, scanner):
    """
    test to raise the exception when standard user gets when tried to edit the scanners
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/131712',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.edit(scanner['id'], force_ui_update=True)


@pytest.mark.xfail(raises=ForbiddenError)
@responses.activate
def test_scanner_edit(tvm, scanner):
    """
    test to raise the exception when doing the edit scanner operation
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/131712',
        json={
            'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
            'created': 1667909255371,
            'modified': 1667984377352,
            'container_uuid': '58962e48-d891-40bb-baba-8b984452328d',
            'uuid': '3e839499-e7a5-4aa5-8a2d-61e621ea343b',
            'id': 131712,
            'name': 'pytenable-scanner',
            'type': 'managed',
            'distributed': True,
            'network_name': 'Default',
            'default_permissions': 16,
            'shared': 1,
            'user_permissions': 128,
            'supports_webapp': False,
            'remote_uuid': 'bdc6b14f-db20-dacb-04e0-960df14350c7834261cf33a01688',
            'key': '00304ce24d16da1ea4e6181e432010eaca13f3394b94c330965b0c0992ad133d',
            'system': False,
            'linked': 1,
            'last_connect': 1667984324837,
            'max_tasks': 50,
            'max_targets': 1499,
            'task_max_targets': 100,
            'platform': 'LINUX',
            'distro': 'ubuntu1110-x86-64',
            'ui_version': '10.4.1',
            'ui_build': '91',
            'engine_version': '19.4.0',
            'loaded_plugin_set': '201812051251',
            'force_plugin_update': 1,
            'hostname': 'pytenable-scanner',
            'settings_pending': False,
            'restart_pending': False,
            'status': 'on',
            'group': False,
            'pvs': False,
            'given_nessus_updates': True,
            'industrial_security': False,
            'lce': False,
            'aws': False,
            'system_scanner_scanner': False,
            'pool': False,
            'cloud_group': False,
            'webapp': False,
            'system_group_scanner': False,
            'can_factory_reset': False,
            'system_webapp_scanner': False,
            'supports_remote_logs': True,
            'supports_remote_settings': True,
            'active_directory': False,
            'scanner_scanner': True,
            'created_in_seconds': 1667909255,
            'modified_in_seconds': 1667984377,
            'network_id': '00000000-0000-0000-0000-000000000000',
        },
    )
    tvm.scanners.edit(scanner['id'], force_plugin_update=True)


@responses.activate
def test_scanner_get_aws_targets_notfounderror(tvm):
    """
    test to raise the exception when aws targets are not found
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/aws-targets',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'Scanner with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanners.get_aws_targets(1)


@pytest.mark.xfail(raises=NotFoundError)
@responses.activate
def test_scanner_get_aws_targets_permissionerror(tvm):
    """
    test to raise the exception when standard user gets the aws targets
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/aws-targets',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'Scanner with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.get_aws_targets(1)


@pytest.mark.skip(reason='No AWS Environment to test against.')
def test_scanner_get_aws_targets(tvm, scanner):
    """
    test to get aws targets
    """
    pass


@responses.activate
def test_scanner_key(tvm, scanner):
    """
    test to verify the instance of scanner key
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/131712/key',
        json={
            'key': '00304ce24d16da1ea4e6181e432010eaca13f3394b94c330965b0c0992ad133d'
        },
    )
    assert isinstance(tvm.scanners.get_scanner_key(scanner['id']), str)


@responses.activate
def test_get_scans_notfounderror(tvm):
    """
    test to raise the exception when the scans are not found
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/scans',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'Scanner with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scanners.get_scans(1)


@responses.activate
def test_get_scans_permissionerror(tvm, scanner):
    """
    test to raise the exception when the standard user gets the scans
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/131712/scans',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.get_scans(scanner['id'])


@responses.activate
def test_get_scans(tvm, scanner):
    """
    test to verify the instance of the scans
    """
    responses.add(
        responses.GET, 'https://nourl/scanners/131712/scans', json={'scans': []}
    )
    assert isinstance(tvm.scanners.get_scans(scanner['id']), list)


@responses.activate
def test_list_scanners_permissionerror(tvm):
    """
    test to raise the exception when standard user gets the list of scanners
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.list()


@responses.activate
def test_list_scanners(tvm):
    """
    test to check the instance of list of scanners
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners',
        json={'scanners': []},
    )
    assert isinstance(tvm.scanners.list(), list)


def test_link_state_linked_typeerror(tvm):
    """
    test to raise the exception when the type of field linked is not as defined
    """
    with pytest.raises(TypeError):
        tvm.scanners.toggle_link_state(1, 'nope')


@responses.activate
def test_link_state_permissionerror(tvm, scanner):
    """
    test to raise the exception when standard user toggle the link state
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/131712/link',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.scanners.toggle_link_state(scanner['id'], True)


@responses.activate
def test_link_state(tvm, scanner):
    """
    test to toggle link state
    """
    responses.add(responses.PUT, 'https://nourl/scanners/131712/link')
    tvm.scanners.toggle_link_state(scanner['id'], True)


@responses.activate
def test_scanners_get_permissions(tvm, scanner):
    """
    test to get the permission
    """
    responses.add(
        responses.GET,
        'https://nourl/permissions/scanner/131712',
        json={
            'acls': [
                {
                    'type': 'user',
                    'id': 1,
                    'uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
                    'name': 'system',
                    'display_name': 'system',
                    'permissions': 128,
                    'owner': 1,
                },
                {'type': 'default', 'permissions': 16},
            ]
        },
    )
    permissions = tvm.scanners.get_permissions(scanner['id'])
    assert isinstance(permissions, list)
    for permission in permissions:
        check(permission, 'type', str)
        check(permission, 'permissions', int)


@responses.activate
def test_scanner_edit_permissions(tvm, scanner, user):
    """
    test to edit the permissions
    """
    responses.add(responses.PUT, 'https://nourl/permissions/scanner/131712')
    tvm.scanners.edit_permissions(
        scanner['id'],
        {'type': 'default', 'permissions': 16},
        {'type': 'user', 'id': user['id'], 'permissions': 16},
    )


@responses.activate
def test_scanner_linking_key(tvm):
    """
    test to get the linking key
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners',
        json={
            'scanners': [
                {
                    'id': 314908,
                    'key': '704d2e3fc8453967a099e76807a852fe279a59b6c50670f17d2d1e212dec484c',
                    'name': 'UK London Cloud Scanners',
                    'uuid': 'c0317d83-342c-41ef-b7cc-ac7411d23eda',
                },
                {
                    'id': 1,
                    'key': 'ffa27c8d0a3f24a8e1ba1b9eaa8b5a35c3a0b1e02c0d1dd1b2cf0c8d2d2a4b6e',
                    'name': 'US Cloud Scanner',
                    'uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                },
            ]
        },
    )
    resp = tvm.scanners.linking_key()
    assert resp == 'ffa27c8d0a3f24a8e1ba1b9eaa8b5a35c3a0b1e02c0d1dd1b2cf0c8d2d2a4b6e'
