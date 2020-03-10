from tenable.errors import *
from ..checker import check, single
import uuid, pytest

@pytest.mark.vcr()
def test_add_scanner_to_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.add_scanner('nope', 1)

@pytest.mark.vcr()
def test_add_scanner_to_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.add_scanner(1, 'nope')

@pytest.mark.vcr()
def test_add_scanner_to_scanner_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.add_scanner(1, 1)

@pytest.mark.vcr()
def test_add_scanner_to_scanner_group_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.add_scanner(1, 1)

@pytest.mark.vcr()
def test_add_scanner_to_group(api, scanner, scannergroup):
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])

@pytest.mark.vcr()
def test_create_scanner_group_name_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.create(1)

@pytest.mark.vcr()
def test_create_scanner_group_type_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.create(str(uuid.uuid4()), group_type=1)

@pytest.mark.vcr()
def test_create_scanner_group_type_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.scanner_groups.create(str(uuid.uuid4()), group_type='normal')

@pytest.mark.vcr()
def test_create_scanner_group_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.create(str(uuid.uuid4()))

@pytest.mark.vcr()
def test_create_scanner_group(api, scannergroup):
    assert isinstance(scannergroup, dict)
    s = scannergroup
    check(s, 'default_permissions', int)
    check(s, 'id', int)
    check(s, 'last_modification_date', int)
    check(s, 'name', str)
    check(s, 'owner', str)
    check(s, 'owner_id', int)
    check(s, 'owner_name', str)
    check(s, 'owner_uuid', 'uuid')
    check(s, 'scan_count', int)
    check(s, 'type', str)
    check(s, 'uuid', 'uuid')

@pytest.mark.vcr()
def test_delete_scanner_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.delete('nope')

@pytest.mark.vcr()
def test_delete_scanner_group_notfound(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.delete(1)

@pytest.mark.vcr()
def test_delete_scanner_group_permissionserror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.delete(1)

@pytest.mark.vcr()
def test_delete_scanner_group(api, scannergroup):
    api.scanner_groups.delete(scannergroup['id'])

@pytest.mark.vcr()
def test_remove_scanner_from_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.delete_scanner('nope', 1)

@pytest.mark.vcr()
def test_remove_scanner_from_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.delete_scanner(1, 'nope')

@pytest.mark.vcr()
def test_remove_scanner_from_scanner_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.delete_scanner(1, 1)

@pytest.mark.vcr()
def test_remove_scanner_from_scanner_group_permissionserror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.delete_scanner(1, 1)

@pytest.mark.vcr()
def test_remove_scanner_from_scanner_group(api, scanner, scannergroup):
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])
    api.scanner_groups.delete_scanner(scannergroup['id'], scanner['id'])

@pytest.mark.vcr()
def test_scannergroup_details_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.details('nope')

@pytest.mark.vcr()
@pytest.mark.xfail(raises=ServerError)
def test_scannergroup_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.details(1)

@pytest.mark.vcr()
def test_scannergroup_details_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.details(1)

@pytest.mark.vcr()
def test_scannergroup_details(api, scannergroup):
    s = api.scanner_groups.details(scannergroup['id'])
    assert s['id'] == scannergroup['id']
    s = scannergroup
    check(s, 'default_permissions', int)
    check(s, 'id', int)
    check(s, 'last_modification_date', int)
    check(s, 'name', str)
    check(s, 'owner', str)
    check(s, 'owner_id', int)
    check(s, 'owner_name', str)
    check(s, 'owner_uuid', 'uuid')
    check(s, 'scan_count', int)
    check(s, 'type', str)
    check(s, 'uuid', 'uuid')

@pytest.mark.vcr()
def test_edit_scanner_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.edit('nope', str(uuid.uuid4()))

@pytest.mark.vcr()
def test_edit_scanner_group_name_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.edit(1, 1)

@pytest.mark.vcr()
@pytest.mark.xfail(raises=ServerError)
def test_edit_scanner_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.edit(1, str(uuid.uuid4()))

@pytest.mark.vcr()
def test_edit_scanner_group_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.edit(1, str(uuid.uuid4()))

@pytest.mark.vcr()
def test_edit_scanner_group(api, scannergroup):
    api.scanner_groups.edit(scannergroup['id'], str(uuid.uuid4()))

@pytest.mark.vcr()
def test_list_scanner_groups(api):
    groups = api.scanner_groups.list()
    assert isinstance(groups, list)
    for s in groups:
        check(s, 'creation_date', int)
        check(s, 'default_permissions', int)
        check(s, 'id', int)
        check(s, 'last_modification_date', int)
        check(s, 'name', str)
        check(s, 'owner', str)
        check(s, 'owner_id', int)
        check(s, 'owner_name', str)
        check(s, 'owner_uuid', 'uuid')
        check(s, 'scan_count', int)
        check(s, 'scanner_count', int)
        check(s, 'scanner_id', int)
        check(s, 'scanner_uuid', 'uuid')
        check(s, 'shared', int)
        check(s, 'type', str)
        check(s, 'user_permissions', int)
        check(s, 'uuid', 'uuid')

@pytest.mark.vcr()
def test_list_scanner_groups_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.list()

@pytest.mark.vcr()
def test_list_scanners_in_scanner_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.list_scanners('nope')

@pytest.mark.vcr()
def test_list_scanners_in_scanner_group_permissionerror(stdapi, scannergroup):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.list_scanners(scannergroup['id'])

@pytest.mark.vcr()
def test_list_scanners_in_scanner_group(api, scannergroup, scanner):
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])
    scanners = api.scanner_groups.list_scanners(scannergroup['id'])
    assert isinstance(scanners, list)
    for s in scanners:
        check(s, 'distro', str, allow_none=True)
        check(s, 'engine_version', str)
        check(s, 'group', bool)
        check(s, 'id', int)
        check(s, 'key', str)
        check(s, 'last_connect', int)
        check(s, 'last_modification_date', int)
        check(s, 'linked', int)
        check(s, 'loaded_plugin_set', str)
        check(s, 'name', str)
        check(s, 'num_hosts', int)
        check(s, 'num_scans', int)
        check(s, 'num_sessions', int)
        check(s, 'num_tcp_sessions', int)
        check(s, 'owner', str)
        check(s, 'owner_id', int)
        check(s, 'owner_name', str)
        check(s, 'owner_uuid', 'uuid')
        check(s, 'platform', str)
        check(s, 'pool', bool)
        check(s, 'scan_count', int)
        check(s, 'source', str)
        check(s, 'status', str)
        check(s, 'timestamp', int)
        check(s, 'type', str)
        check(s, 'ui_build', str)
        check(s, 'ui_version', str)
        check(s, 'uuid', 'uuid')
    api.scanner_groups.delete_scanner(scannergroup['id'], scanner['id'])