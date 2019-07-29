from tenable.errors import *
from ..checker import check, single
import pytest, uuid

@pytest.fixture
def network(request, api, vcr):
    with vcr.use_cassette('test_networks_create_success'):
        network = api.networks.create('Example')
    def teardown():
        try:
            with vcr.use_cassette('test_networks_delete_success'):
                api.networks.delete(network['uuid'])
        except APIError:
            pass
    request.addfinalizer(teardown)
    return network

def test_networks_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.create(1, 'something')

def test_networks_create_description_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.create('something', 1)

@pytest.mark.vcr()
def test_networks_create_success(api, network):
    assert isinstance(network, dict)
    check(network, 'owner_uuid', 'uuid')
    check(network, 'created', int)
    check(network, 'modified', int)
    check(network, 'scanner_count', int)
    check(network, 'uuid', 'uuid')
    check(network, 'name', str)
    check(network, 'description', str)
    check(network, 'is_default', bool)
    check(network, 'created_by', 'uuid')
    check(network, 'modified_by', 'uuid')
    check(network, 'created_in_seconds', int)
    check(network, 'modified_in_seconds', int)

def test_networks_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.delete(1)

def test_networks_delete_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.delete('something')

@pytest.mark.vcr()
def test_networks_delete_success(api, network):
    api.networks.delete(network['uuid'])

def test_networks_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.details(1)

def test_networks_details_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.details('something')

@pytest.mark.vcr()
def test_networks_details_success(api, network):
    n = api.networks.details(network['uuid'])
    assert isinstance(n, dict)
    check(n, 'owner_uuid', 'uuid')
    check(n, 'created', int)
    check(n, 'modified', int)
    check(n, 'scanner_count', int)
    check(n, 'uuid', 'uuid')
    check(n, 'name', str)
    check(n, 'description', str)
    check(n, 'is_default', bool)
    check(n, 'created_by', 'uuid')
    check(n, 'modified_by', 'uuid')
    check(n, 'created_in_seconds', int)
    check(n, 'modified_in_seconds', int)

def test_networks_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.edit(1, 'something')

def test_networks_edit_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.edit('something', 'something')

def test_networks_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.edit(str(uuid.uuid4()), 1)

def test_networks_edit_description_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.edit(str(uuid.uuid4()), 'something', 1)

@pytest.mark.vcr()
def test_networks_edit_success(api, network):
    n = api.networks.edit(network['uuid'], 'New Name')
    assert isinstance(n, dict)
    check(n, 'owner_uuid', 'uuid')
    check(n, 'created', int)
    check(n, 'modified', int)
    check(n, 'scanner_count', int)
    check(n, 'uuid', 'uuid')
    check(n, 'name', str)
    check(n, 'description', str)
    check(n, 'is_default', bool)
    check(n, 'created_by', 'uuid')
    check(n, 'modified_by', 'uuid')
    check(n, 'created_in_seconds', int)
    check(n, 'modified_in_seconds', int)

def test_networks_list_scanners_id_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list_scanners(1)

def test_networks_list_scanners_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.list_scanners('something')

@pytest.mark.vcr()
def test_networks_list_scanners_success(api):
    scanners = api.networks.list_scanners('00000000-0000-0000-0000-000000000000')
    assert isinstance(scanners, list)
    for s in scanners:
        assert isinstance(s, dict)
        check(s, 'owner_uuid', 'uuid')
        check(s, 'uuid', 'scanner-uuid')
        check(s, 'id', int)
        check(s, 'name', str)
        check(s, 'key', str)
        check(s, 'status', str)
        check(s, 'group', bool)

def test_networks_unassigned_scanners_id_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.unassigned_scanners(1)

def test_networks_unassigned_scanners_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.unassigned_scanners('something')

@pytest.mark.vcr()
def test_networks_unassigned_scanners_success(api, network):
    scanners = api.networks.unassigned_scanners(network['uuid'])
    assert isinstance(scanners, list)
    for s in scanners:
        assert isinstance(s, dict)
        check(s, 'owner_uuid', 'uuid')
        check(s, 'uuid', 'scanner-uuid')
        check(s, 'id', int)
        check(s, 'name', str)
        check(s, 'key', str)
        check(s, 'status', str)
        check(s, 'group', bool)

def test_networks_assign_scanners_id_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.assign_scanners(1, str(uuid.uuid4()))

def test_networks_assign_scanners_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.assign_scanners('something', str(uuid.uuid4()))

def test_networks_assign_scanners_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.assign_scanners(str(uuid.uuid4()), 1)

def test_networks_assign_scanners_scanner_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.assign_scanners(str(uuid.uuid4()), 'something')

@pytest.mark.vcr()
def test_networks_assign_scanners_success(api, network, vcr):
    with vcr.use_cassette('test_networks_list_scanners_success'):
        scanner = api.networks.list_scanners(
            '00000000-0000-0000-0000-000000000000')[0]
    api.networks.assign_scanners(network['uuid'], scanner['uuid'])

@pytest.mark.vcr()
def test_networks_list_offset_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(offset='nope')

@pytest.mark.vcr()
def test_networks_list_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(limit='nope')

@pytest.mark.vcr()
def test_networks_list_sort_field_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(sort=((1, 'asc'),))

@pytest.mark.vcr()
def test_networks_list_sort_direction_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(sort=(('uuid', 1),))

@pytest.mark.vcr()
def test_networks_list_sort_direction_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.networks.list(sort=(('uuid', 'nope'),))

@pytest.mark.vcr()
def test_networks_list_filter_name_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list((1, 'match', 'win'))

@pytest.mark.vcr()
def test_networks_list_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(('name', 1, 'win'))

@pytest.mark.vcr()
def test_networks_list_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(('name', 'match', 1))

@pytest.mark.vcr()
def test_networks_list_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(filter_type=1)

@pytest.mark.vcr()
def test_networks_list_wildcard_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(wildcard=1)

@pytest.mark.vcr()
def test_networks_list_wildcard_fields_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(wildcard_fields='nope')

@pytest.mark.vcr()
def test_networks_list_include_deleted_typeerror(api):
    with pytest.raises(TypeError):
        api.networks.list(include_deleted='nope')

@pytest.mark.vcr()
def test_networks_list(api):
    count = 0
    networks = api.networks.list()
    for i in networks:
        count += 1
        assert isinstance(i, dict)
        check(i, 'owner_uuid', 'uuid')
        check(i, 'created', int)
        check(i, 'modified', int)
        check(i, 'scanner_count', int)
        check(i, 'uuid', 'uuid')
        check(i, 'name', str)
        check(i, 'is_default', bool)
        check(i, 'created_by', 'uuid')
        check(i, 'modified_by', 'uuid')
        check(i, 'created_in_seconds', int)
        check(i, 'modified_in_seconds', int)
    assert count == networks.total