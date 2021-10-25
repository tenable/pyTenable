'''
test scanner_groups
'''
import uuid
import pytest
from tenable.errors import BadRequestError, ForbiddenError, \
    NotFoundError, UnexpectedValueError, ServerError
from tests.checker import check

@pytest.mark.vcr()
def test_add_scanner_to_group_group_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.add_scanner('nope', 1)

@pytest.mark.vcr()
def test_add_scanner_to_group_scanner_id_typeerror(api):
    '''
    test to raise exception when type of scanner_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.add_scanner(1, 'nope')

@pytest.mark.vcr()
def test_add_scanner_to_scanner_group_notfounderror(api):
    '''
    test to raise exception when scanner_id or group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scanner_groups.add_scanner(1, 1)

@pytest.mark.vcr()
def test_add_scanner_to_scanner_group_permissionerror(stdapi):
    '''
    test to raise exception when standard user try to add scanner to group.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.add_scanner(1, 1)

@pytest.mark.vcr()
def test_add_scanner_to_group(api, scanner, scannergroup):
    '''
    test to add scanner to scanner_group
    '''
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])

@pytest.mark.vcr()
def test_create_scanner_group_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.create(1)

@pytest.mark.vcr()
def test_create_scanner_group_type_typeerror(api):
    '''
    test to raise exception when type of group_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.create(str(uuid.uuid4()), group_type=1)

@pytest.mark.vcr()
def test_create_scanner_group_type_unexpectedvalue(api):
    '''
    test to raise exception when group_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scanner_groups.create(str(uuid.uuid4()), group_type='normal')

@pytest.mark.vcr()
def test_create_scanner_group_permissionerror(stdapi):
    '''
    test to raise exception when standard user try to create scanner group.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.create(str(uuid.uuid4()))

@pytest.mark.vcr()
def test_create_scanner_group(scannergroup):
    '''
    test to create scanner_group
    '''
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

@pytest.mark.vcr()
def test_delete_scanner_group_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.delete('nope')

@pytest.mark.vcr()
def test_delete_scanner_group_notfound(api):
    '''
    test to raise exception when user provided group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scanner_groups.delete(1)

@pytest.mark.vcr()
def test_delete_scanner_group_permissionserror(stdapi):
    '''
    test to raise exception when standard user try to delete scanner group.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.delete(1)

@pytest.mark.vcr()
def test_delete_scanner_group(api, scannergroup):
    '''
    test to delete scanner_group
    '''
    api.scanner_groups.delete(scannergroup['id'])

@pytest.mark.vcr()
def test_remove_scanner_from_group_group_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.delete_scanner('nope', 1)

@pytest.mark.vcr()
def test_remove_scanner_from_group_scanner_id_typeerror(api):
    '''
    test to raise exception when type of scanner_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.delete_scanner(1, 'nope')

@pytest.mark.vcr()
def test_remove_scanner_from_scanner_group_notfounderror(api):
    '''
    test to raise exception when scanner_id or group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scanner_groups.delete_scanner(1, 1)

@pytest.mark.vcr()
def test_remove_scanner_from_scanner_group_permissionserror(stdapi):
    '''
    test to raise exception when standard user try to remove scanner from scanner group.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.delete_scanner(1, 1)

@pytest.mark.vcr()
def test_remove_scanner_from_scanner_group(api, scanner, scannergroup):
    '''
    test to remove scanner from scanner group
    '''
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])
    api.scanner_groups.delete_scanner(scannergroup['id'], scanner['id'])

@pytest.mark.vcr()
def test_scannergroup_details_group_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.details('nope')

@pytest.mark.vcr()
@pytest.mark.xfail(raises=ServerError)
def test_scannergroup_details_notfounderror(api):
    '''
    test to raise exception when group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scanner_groups.details(1)

@pytest.mark.vcr()
def test_scannergroup_details_permissionerror(stdapi):
    '''
    test to raise exception when standard user try to get details of scanner group.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.details(1)

@pytest.mark.vcr()
def test_scannergroup_details(api, scannergroup):
    '''
    test to get details of scanner group.
    '''
    scanner_group = api.scanner_groups.details(scannergroup['id'])
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

@pytest.mark.vcr()
def test_edit_scanner_group_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.edit('nope', str(uuid.uuid4()))

@pytest.mark.vcr()
def test_edit_scanner_group_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.edit(1, 1)

@pytest.mark.vcr()
@pytest.mark.xfail(raises=ServerError)
def test_edit_scanner_group_notfounderror(api):
    '''
    test to raise exception when group_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scanner_groups.edit(1, str(uuid.uuid4()))

@pytest.mark.vcr()
def test_edit_scanner_group_permissionerror(stdapi):
    '''
    test to raise exception when standard user try to edit name of scanner group.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.edit(1, str(uuid.uuid4()))

@pytest.mark.vcr()
def test_edit_scanner_group(api, scannergroup):
    '''
    test to edit scanner group
    '''
    api.scanner_groups.edit(scannergroup['id'], str(uuid.uuid4()))

@pytest.mark.vcr()
def test_list_scanner_groups(api):
    '''
    test to list scanner group
    '''
    groups = api.scanner_groups.list()
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

@pytest.mark.vcr()
def test_list_scanner_groups_permissionerror(stdapi):
    '''
    test to raise exception when standard user try to get list of scanner groups.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.list()

@pytest.mark.vcr()
def test_list_scanners_in_scanner_group_id_typeerror(api):
    '''
    test to raise exception when type of group_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.list_scanners('nope')

@pytest.mark.vcr()
def test_list_scanners_in_scanner_group_permissionerror(stdapi, scannergroup):
    '''
    test to raise exception when standard user try to get list of scanners in scanner groups.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.scanner_groups.list_scanners(scannergroup['id'])

@pytest.mark.vcr()
def test_list_scanners_in_scanner_group(api, scannergroup, scanner):
    '''
    test to get list of scanners in scanner group
    '''
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])
    scanners = api.scanner_groups.list_scanners(scannergroup['id'])
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
    api.scanner_groups.delete_scanner(scannergroup['id'], scanner['id'])

@pytest.mark.vcr()
def test_edit_routes_in_scanner_group_invalidinputerror(api, scannergroup):
    '''
    test to raise exception when values in routes are invalid
    '''
    with pytest.raises(BadRequestError):
        api.scanner_groups.edit_routes(scannergroup['id'], ['127.0.0.256'])

@pytest.mark.vcr()
def test_edit_routes_in_scanner_group_typeerror(api, scannergroup):
    '''
    test to raise exception when type of routes param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scanner_groups.edit_routes(scannergroup['id'], '127.0.0.1')

@pytest.mark.vcr()
def test_edit_routes_in_scanner_group_success(api, scannergroup):
    '''
    test to edit routes in scanner group
    '''
    api.scanner_groups.edit_routes(scannergroup['id'], ['127.0.0.1'])

@pytest.mark.vcr()
def test_list_routes_in_scanner_group_success(api, scannergroup):
    '''
    test to list routes in scanner group
    '''
    api.scanner_groups.edit_routes(scannergroup['id'], ['127.0.0.1'])
    routes = api.scanner_groups.list_routes(scannergroup['id'])
    assert routes[0]['route'] == '127.0.0.1'
