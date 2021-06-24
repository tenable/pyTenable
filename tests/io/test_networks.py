'''
test networks
'''
import uuid
import pytest
from tenable.errors import UnexpectedValueError, APIError, InvalidInputError
from tests.checker import check

@pytest.fixture(name='network')
def fixture_network(request, api, vcr):
    '''
    Fixture to create network
    '''
    with vcr.use_cassette('test_networks_create_success'):
        network = api.networks.create('Network-{}'.format(uuid.uuid4()))
    def teardown():
        '''
        cleanup function to delete network
        '''
        try:
            with vcr.use_cassette('test_networks_delete_success'):
                api.networks.delete(network['uuid'])
        except APIError:
            pass
    request.addfinalizer(teardown)
    return network

def test_networks_create_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.create(1, 'something')

def test_networks_create_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.create('something', 1)

@pytest.mark.vcr()
def test_networks_create_success(network):
    '''
    test to create network.
    '''
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
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.delete(1)

def test_networks_delete_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of network_id param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.delete('something')

@pytest.mark.vcr()
def test_networks_delete_success(api, network):
    '''
    test to delete network.
    '''
    api.networks.delete(network['uuid'])

def test_networks_details_id_typeerror(api):
    '''
    test to raise exception when type of network param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.details(1)

def test_networks_details_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of network_id param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.details('something')

@pytest.mark.vcr()
def test_networks_details_success(api, network):
    '''
    test to get details of specified network.
    '''
    resp = api.networks.details(network['uuid'])
    assert isinstance(resp, dict)
    check(resp, 'owner_uuid', 'uuid')
    check(resp, 'created', int)
    check(resp, 'modified', int)
    check(resp, 'scanner_count', int)
    check(resp, 'uuid', 'uuid')
    check(resp, 'name', str)
    check(resp, 'description', str)
    check(resp, 'is_default', bool)
    check(resp, 'created_by', 'uuid')
    check(resp, 'modified_by', 'uuid')
    check(resp, 'created_in_seconds', int)
    check(resp, 'modified_in_seconds', int)

def test_networks_edit_id_typeerror(api):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.edit(1, 'something')

def test_networks_edit_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of network_id param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.edit('something', 'something')

def test_networks_edit_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.edit(str(uuid.uuid4()), 1)

def test_networks_edit_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.edit(str(uuid.uuid4()), 'something', 1)

@pytest.mark.vcr()
def test_networks_edit_success(api, network):
    '''
    test to update the specified network resource.
    '''
    resp = api.networks.edit(network['uuid'], 'New Name - {}'.format(uuid.uuid4()))
    assert isinstance(resp, dict)
    check(resp, 'owner_uuid', 'uuid')
    check(resp, 'created', int)
    check(resp, 'modified', int)
    check(resp, 'scanner_count', int)
    check(resp, 'uuid', 'uuid')
    check(resp, 'name', str)
    check(resp, 'description', str)
    check(resp, 'is_default', bool)
    check(resp, 'created_by', 'uuid')
    check(resp, 'modified_by', 'uuid')
    check(resp, 'created_in_seconds', int)
    check(resp, 'modified_in_seconds', int)

def test_networks_list_scanners_id_typeerror(api):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list_scanners(1)

def test_networks_list_scanners_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of network_id param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.list_scanners('something')

@pytest.mark.vcr()
def test_networks_list_scanners_success(api):
    '''
    test to get list of scanners associated to given network.
    '''
    scanners = api.networks.list_scanners('00000000-0000-0000-0000-000000000000')
    assert isinstance(scanners, list)
    for scanner in scanners:
        assert isinstance(scanner, dict)
        check(scanner, 'owner_uuid', 'uuid')
        check(scanner, 'uuid', 'scanner-uuid')
        check(scanner, 'id', int)
        check(scanner, 'name', str)
        check(scanner, 'key', str)
        check(scanner, 'status', str)
        check(scanner, 'group', bool)

def test_networks_unassigned_scanners_id_typeerror(api):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.unassigned_scanners(1)

def test_networks_unassigned_scanners_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of network_id param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.unassigned_scanners('something')

@pytest.mark.vcr()
def test_networks_unassigned_scanners_success(api, network):
    '''
    test to get the list of scanners that are currently unassigned to the given network
    '''
    scanners = api.networks.unassigned_scanners(network['uuid'])
    assert isinstance(scanners, list)
    for scanner in scanners:
        assert isinstance(scanner, dict)
        check(scanner, 'owner_uuid', 'uuid')
        check(scanner, 'uuid', 'scanner-uuid')
        check(scanner, 'id', int)
        check(scanner, 'name', str)
        check(scanner, 'key', str)
        check(scanner, 'status', str)
        check(scanner, 'group', bool)

def test_networks_assign_scanners_id_typeerror(api):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.assign_scanners(1, str(uuid.uuid4()))

def test_networks_assign_scanners_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of network_id param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.assign_scanners('something', str(uuid.uuid4()))

def test_networks_assign_scanners_scanner_id_typeerror(api):
    '''
    test to raise exception when type of scanner_uuis param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.assign_scanners(str(uuid.uuid4()), 1)

def test_networks_assign_scanners_scanner_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of scanner_uuid param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.assign_scanners(str(uuid.uuid4()), 'something')

@pytest.mark.vcr()
def test_networks_assign_scanners_success(api, network, vcr):
    '''
    test to assign scanners to network.
    '''
    with vcr.use_cassette('test_networks_list_scanners_success'):
        scanner = api.networks.list_scanners(
            '00000000-0000-0000-0000-000000000000')[0]
    api.networks.assign_scanners(network['uuid'], scanner['uuid'])

@pytest.mark.vcr()
def test_networks_list_offset_typeerror(api):
    '''
    test to raise exception when type of offset param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(offset='nope')

@pytest.mark.vcr()
def test_networks_list_limit_typeerror(api):
    '''
    test to raise exception when type of limit param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(limit='nope')

@pytest.mark.vcr()
def test_networks_list_sort_field_typeerror(api):
    '''
    test to raise exception when type of sort field param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(sort=((1, 'asc'),))

@pytest.mark.vcr()
def test_networks_list_sort_direction_typeerror(api):
    '''
    test to raise exception when type of sort direction param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(sort=(('uuid', 1),))

@pytest.mark.vcr()
def test_networks_list_sort_direction_unexpectedvalue(api):
    '''
    test to raise exception when value of sort direction param does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.list(sort=(('uuid', 'nope'),))

@pytest.mark.vcr()
def test_networks_list_filter_name_typeerror(api):
    '''
    test to raise exception when type of filter_name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list((1, 'match', 'win'))

@pytest.mark.vcr()
def test_networks_list_filter_operator_typeerror(api):
    '''
    test to raise exception when type of filter_operator param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(('name', 1, 'win'))

@pytest.mark.vcr()
def test_networks_list_filter_value_typeerror(api):
    '''
    test to raise exception when type of filter_value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(('name', 'match', 1))

@pytest.mark.vcr()
def test_networks_list_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(filter_type=1)

@pytest.mark.vcr()
def test_networks_list_wildcard_typeerror(api):
    '''
    test to raise exception when type of wildcard param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(wildcard=1)

@pytest.mark.vcr()
def test_networks_list_wildcard_fields_typeerror(api):
    '''
    test to raise exception when type of wildcard_fields param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(wildcard_fields='nope')

@pytest.mark.vcr()
def test_networks_list_include_deleted_typeerror(api):
    '''
    test to raise exception when type of include_deleted param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.list(include_deleted='nope')

@pytest.mark.vcr()
def test_networks_list(api):
    '''
    test to get list of configured networks.
    '''
    count = 0
    networks = api.networks.list()
    for network in networks:
        count += 1
        assert isinstance(network, dict)
        check(network, 'owner_uuid', 'uuid')
        check(network, 'created', int)
        check(network, 'modified', int)
        check(network, 'scanner_count', int)
        check(network, 'uuid', 'uuid')
        check(network, 'name', str)
        check(network, 'is_default', bool)
        check(network, 'created_by', 'uuid')
        check(network, 'modified_by', 'uuid')
        check(network, 'created_in_seconds', int)
        check(network, 'modified_in_seconds', int)
    assert count == networks.total

@pytest.mark.vcr()
def test_network_asset_count_network_id_typeerror(api):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.network_asset_count(1, 180)

@pytest.mark.vcr()
def test_network_asset_count_network_id_unexpectedvalueerror(api):
    '''
    test to raise exception when value of network_id param does not match the expected pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.network_asset_count('nope', 180)

@pytest.mark.vcr()
def test_network_asset_count_network_num_days_typeerror(api):
    '''
    test to raise exception when type of num_days param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.networks.network_asset_count('00000000-0000-0000-0000-000000000000', 'nope')

@pytest.mark.vcr()
def test_network_asset_count_network_num_days_invalidinputerror(api):
    '''
    test to raise exception when value of num_days param is not valid.
    '''
    with pytest.raises(InvalidInputError):
        api.networks.network_asset_count('00000000-0000-0000-0000-000000000000', -180)

@pytest.mark.vcr()
def test_network_asset_count_network_success(api):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    network = '00000000-0000-0000-0000-000000000000'
    resp = api.networks.network_asset_count(network, 180)
    assert isinstance(resp, dict)
    check(resp, 'numAssetsTotal', int)
    check(resp, 'numAssetsNotSeen', int)

@pytest.mark.vcr()
def test_networks_assign_multiple_scanners_success(api, network, scanner):
    '''
    test to pass multiple scanners
    '''
    scanner = api.networks.list_scanners('00000000-0000-0000-0000-000000000000')[0]
    api.networks.assign_scanners(network['uuid'], scanner['uuid'], scanner['uuid'])


@pytest.mark.vcr()
def test_networks_unexpectedvalueerror(api, network):
    '''
    test to raise exception when scanner_uuids are not passed

    '''
    with pytest.raises(UnexpectedValueError):
        api.networks.assign_scanners(network['uuid'])

@pytest.mark.vcr()
def test_networks_list_fileds(api):
    '''
    test to get list of configured networks.
    '''
    count = 0
    networks = api.networks.list(filter_type='or',
                                 include_deleted=True,
                                 offset=2,
                                 limit=50,
                                 wildcard='match',
                                 wildcard_fields=['name'])
    for network in networks:
        assert isinstance(network, dict)
        check(network, 'owner_uuid', 'uuid')
        check(network, 'created', int)
        check(network, 'modified', int)
        check(network, 'scanner_count', int)
        check(network, 'uuid', 'uuid')
        check(network, 'name', str)
        check(network, 'is_default', bool)
        check(network, 'created_by', 'uuid')
        check(network, 'modified_by', 'uuid')
        check(network, 'created_in_seconds', int)
        check(network, 'modified_in_seconds', int)
