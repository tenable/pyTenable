from .fixtures import *
from tenable.errors import *
import uuid

def test_add_scanner_to_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.add_scanner('nope', 1)

def test_add_scanner_to_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.add_scanner(1, 'nope')

def test_add_scanner_to_scanner_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.add_scanner(1, 1)

def test_add_scanner_to_scanner_group_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.add_scanner(1, 1)

def test_add_scanner_to_group(api, scanner, scannergroup):
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])

def test_create_scanner_group_name_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.create(1)

def test_create_scanner_group_type_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.create(str(uuid.uuid4()), group_type=1)

def test_create_scanner_group_type_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.scanner_groups.create(str(uuid.uuid4()), group_type='normal')

def test_create_scanner_group_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.create(str(uuid.uuid4()))

def test_create_scanner_group(api, scannergroup):
    assert isinstance(scannergroup, dict)

def test_delete_scanner_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.delete('nope')

def test_delete_scanner_group_notfound(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.delete(1)

def test_delete_scanner_group_permissionserror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.delete(1)

def test_delete_scanner_group(api, scannergroup):
    api.scanner_groups.delete(scannergroup['id'])

def test_remove_scanner_from_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.delete_scanner('nope', 1)

def test_remove_scanner_from_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.delete_scanner(1, 'nope')

def test_remove_scanner_from_scanner_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.delete_scanner(1, 1)

def test_remove_scanner_from_scanner_group_permissionserror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.delete_scanner(1, 1)

def test_remove_scanner_from_scanner_group(api, scanner, scannergroup):
    api.scanner_groups.add_scanner(scannergroup['id'], scanner['id'])
    api.scanner_groups.delete_scanner(scannergroup['id'], scanner['id'])

def test_details_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.details('nope')

@pytest.mark.xfail(raises=ServerError)
def test_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.details(1)

def test_details_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.details(1)

def test_details(api, scannergroup):
    dets = api.scanner_groups.details(scannergroup['id'])
    assert dets['id'] == scannergroup['id']

def test_edit_scanner_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.edit('nope', str(uuid.uuid4()))

def test_edit_scanner_group_name_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.edit(1, 1)

def test_edit_scanner_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scanner_groups.edit(1, str(uuid.uuid4()))

def test_edit_scanner_group_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.edit(1, str(uuid.uuid4()))

def test_edit_scanner_group(api, scannergroup):
    api.scanner_groups.edit(scannergroup['id'], str(uuid.uuid4()))

def test_list_scanner_groups(api):
    assert isinstance(api.scanner_groups.list(), list)

def test_list_scanner_groups_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.list()

def test_list_scanners_in_scanner_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scanner_groups.list_scanners('nope')

def test_list_scanners_in_scanner_group_permissionerror(stdapi, scannergroup):
    with pytest.raises(PermissionError):
        stdapi.scanner_groups.list_scanners(scannergroup['id'])

def test_list_scanners_in_scanner_group(api, scannergroup):
    assert isinstance(api.scanner_groups.list_scanners(scannergroup['id']), list)