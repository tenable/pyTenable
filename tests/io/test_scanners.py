'''
test scanners
'''
import uuid
import pytest
from tenable.errors import NotFoundError, UnexpectedValueError, ForbiddenError
from ..checker import check


@pytest.mark.vcr()
def test_scanner_control_scans_scanner_id_typeerror(api):
    '''
    test to raise the exception when the type of field scanner_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.control_scan('nope', str(uuid.uuid4()), 'stop')


@pytest.mark.vcr()
def test_scanner_control_scans_scan_uuid_typeerror(api):
    '''
    test to raise the exception when the type of field scan_uuid is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.control_scan(1, 1, 'stop')


@pytest.mark.vcr()
def test_scanner_control_scans_action_typeerror(api):
    '''
    test to raise the exception when the type of field action is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.control_scan(1, str(uuid.uuid4()), 1)


@pytest.mark.vcr()
def test_scanner_control_scans_action_unexpectedvalue(api):
    '''
    test to raise the exception when performed action on the scanner which is not found
    '''
    with pytest.raises(UnexpectedValueError):
        api.scanners.control_scan(1, str(uuid.uuid4()), 'nope')


@pytest.mark.vcr()
def test_scanner_control_scans_notfounderror(api):
    '''
    test to raise the exception when the standard user performs actions against
    scanner which is not found
    '''
    with pytest.raises(NotFoundError):
        api.scanners.control_scan(1,
                                  'c5e3e4c9-ee47-4fbc-9e1d-d6f39801f56c', 'stop')


@pytest.mark.vcr()
def test_scanner_control_scans_permissionerror(stdapi):
    '''
    test to raise the exception when standard user performs actions against
    given scanner
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.control_scan(1,
                                     'c5e3e4c9-ee47-4fbc-9e1d-d6f39801f56c', 'stop')


@pytest.mark.vcr()
def test_scanner_delete_id_typeerror(api):
    '''
    test to raise the exception when the type of field id is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.delete('nope')


@pytest.mark.vcr()
def test_scanner_delete_notfound(api):
    '''
    test to raise the exception when the id is not found to delete the scanner
    '''
    with pytest.raises(NotFoundError):
        api.scanners.delete(1)


@pytest.mark.vcr()
def test_scanner_delete_permissionerror(stdapi, scanner):
    '''
    test to raise the exception when the standard user gets when tried to delete the scanner
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.delete(scanner['id'])


@pytest.mark.skip(reason="We don't want to actually delete scanners.")
def test_scanner_delete(api, scanner):
    '''
    test to delete the scanners
    '''
    api.scanners.delete(scanner['id'])


@pytest.mark.vcr()
def test_scanner_details_id_typeerror(api):
    '''
    test to raise the exception when the type of field id is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.details('nope')


@pytest.mark.vcr()
def test_scanner_details_notfounderror(api):
    '''
    test to raise the exception when the details of the scanners not found
    '''
    with pytest.raises(NotFoundError):
        api.scanners.details(1)


@pytest.mark.vcr()
def test_scanner_details_permissionerror(stdapi, scanner):
    '''
    test to raise the exception when standatd user tries to get the details
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.details(scanner['id'])


@pytest.mark.vcr()
def test_scanner_details(api, scanner):
    '''
    test to get the scanner details
    '''
    each_scanner = api.scanners.details(scanner['id'])
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


@pytest.mark.vcr()
def test_scanner_edit_id_typeerror(api):
    '''
    test to raise the exception when the type of field id is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.edit('nope')


@pytest.mark.vcr()
def test_sanner_edit_plugin_update_typeerror(api, scanner):
    '''
    test to raise the exception when the type of field force_plugin_update is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.edit(scanner['id'], force_plugin_update='yup')


@pytest.mark.vcr()
def test_scanner_edit_ui_update_typeerror(api, scanner):
    '''
    test to raise the exception when the type of field force_ui_update is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.edit(scanner['id'], force_ui_update='yup')


@pytest.mark.vcr()
def test_scanner_edit_finish_update_typeerror(api, scanner):
    '''
    test to raise the exception when the type of field finish_update is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.edit(scanner['id'], finish_update='yup')


@pytest.mark.vcr()
def test_scanner_edit_registration_code_typeerror(api, scanner):
    '''
    test to raise the exception when the type of field registration_code is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.edit(scanner['id'], registration_code=False)


@pytest.mark.vcr()
def test_scanner_edit_aws_update_typeerror(api, scanner):
    '''
    test to raise the exception when the type of field aws update interval is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.edit(scanner['id'], aws_update_interval='nope')


@pytest.mark.vcr()
@pytest.mark.xfail(raises=ForbiddenError)
def test_scanner_edit_notfounderror(api):
    '''
    test to raise the exception when tried to edit the scanner which is not found
    '''
    with pytest.raises(NotFoundError):
        api.scanners.edit(1, force_ui_update=True)


@pytest.mark.vcr()
def test_scanner_edit_permissionserror(stdapi, scanner):
    '''
    test to raise the exception when standard user gets when tried to edit the scanners
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.edit(scanner['id'], force_ui_update=True)


@pytest.mark.vcr()
@pytest.mark.xfail(raises=ForbiddenError)
def test_scanner_edit(api, scanner):
    '''
    test to raise the exception when doing the edit scanner operation
    '''
    api.scanners.edit(scanner['id'], force_plugin_update=True)


@pytest.mark.vcr()
def test_scanner_get_aws_targets_id_typeerror(api):
    '''
    test to raise the exception when the type of field id in aws targets is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.get_aws_targets('nope')


@pytest.mark.vcr()
def test_scanner_get_aws_targets_notfounderror(api):
    '''
    test to raise the exception when aws targets are not found
    '''
    with pytest.raises(NotFoundError):
        api.scanners.get_aws_targets(1)


@pytest.mark.vcr()
@pytest.mark.xfail(raises=NotFoundError)
def test_scanner_get_aws_targets_permissionerror(stdapi):
    '''
    test to raise the exception when standard user gets the aws targets
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.get_aws_targets(1)


@pytest.mark.skip(reason="No AWS Environment to test against.")
@pytest.mark.vcr()
def test_scanner_get_aws_targets(api, scanner):
    '''
    test to get aws targets
    '''
    pass


@pytest.mark.vcr()
def test_scanner_key_id_typeerror(api):
    '''
    test to raise the exception when the type of field scanner_key id is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.get_scanner_key('nope')


@pytest.mark.vcr()
def test_scanner_key(api, scanner):
    '''
    test to verify the instance of scanner key
    '''
    assert isinstance(api.scanners.get_scanner_key(scanner['id']), str)


@pytest.mark.vcr()
def test_get_scans_id_typeerror(api):
    '''
    test to raise the exception when the type of field id is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.get_scans('nope')


@pytest.mark.vcr()
def test_get_scans_notfounderror(api):
    '''
    test to raise the exception when the scans are not found
    '''
    with pytest.raises(NotFoundError):
        api.scanners.get_scans(1)


@pytest.mark.vcr()
def test_get_scans_permissionerror(stdapi, scanner):
    '''
    test to raise the exception when the standard user gets the scans
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.get_scans(scanner['id'])


@pytest.mark.vcr()
def test_get_scans(api, scanner):
    '''
    test to verify the instance of the scans
    '''
    assert isinstance(api.scanners.get_scans(scanner['id']), list)


@pytest.mark.vcr()
def test_list_scanners_permissionerror(stdapi):
    '''
    test to raise the exception when standard user gets the list of scanners
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.list()


@pytest.mark.vcr()
def test_list_scanners(api):
    '''
    test to check the instance of list of scanners
    '''
    assert isinstance(api.scanners.list(), list)


@pytest.mark.vcr()
def test_link_state_id_typeerror(api):
    '''
    test to raise the exception when the type of field id is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.toggle_link_state('nope', True)


@pytest.mark.vcr()
def test_link_state_linked_typeerror(api):
    '''
    test to raise the exception when the type of field linked is not as defined
    '''
    with pytest.raises(TypeError):
        api.scanners.toggle_link_state(1, 'nope')


@pytest.mark.vcr()
def test_link_state_permissionerror(stdapi, scanner):
    '''
    test to raise the exception when standard user toggle the link state
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanners.toggle_link_state(scanner['id'], True)


@pytest.mark.vcr()
def test_link_state(api, scanner):
    '''
    test to toggle link state
    '''
    api.scanners.toggle_link_state(scanner['id'], True)


@pytest.mark.vcr()
def test_scanners_get_permissions(api, scanner):
    '''
    test to get the permission
    '''
    permissions = api.scanners.get_permissions(scanner['id'])
    assert isinstance(permissions, list)
    for permission in permissions:
        check(permission, 'type', str)
        check(permission, 'permissions', int)


@pytest.mark.vcr()
def test_scanner_edit_permissions(api, scanner, user):
    '''
    test to edit the permissions
    '''
    api.scanners.edit_permissions(scanner['id'],
                                  {'type': 'default', 'permissions': 16},
                                  {'type': 'user', 'id': user['id'], 'permissions': 16})


@pytest.mark.vcr()
def test_scanner_linking_key(api):
    '''
    test to get the linking key
    '''
    resp = api.scanners.linking_key()
    assert isinstance(resp, str)
