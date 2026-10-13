"""
test networks
"""

import uuid

import pytest
import responses
from responses import matchers

from tenable.errors import BadRequestError, UnexpectedValueError
from tests.checker import check

NETWORKS_SCANNERS = {
    'scanners': [
        {
            'creation_date': 1614599787,
            'group': True,
            'id': 314908,
            'key': '704d2e3fc8453967a099e76807a852fe279a59b6c50670f17d2d1e212dec484c',
            'last_connect': None,
            'last_modification_date': 1614599787,
            'linked': 1,
            'name': 'UK London Cloud Scanners',
            'num_scans': 0,
            'owner': 'system',
            'owner_id': 2201486,
            'owner_name': 'system',
            'owner_uuid': 'e2302807-7a65-4ad4-908a-5e8b8c9965e6',
            'pool': True,
            'scan_count': 0,
            'source': 'service',
            'status': 'on',
            'timestamp': 1614599787,
            'type': 'local',
            'uuid': 'c0317d83-342c-41ef-b7cc-ac7411d23eda',
            'supports_remote_logs': False,
        }
    ]
}


@responses.activate
def test_networks_create_success(tvm, network):
    """
    test to create network.
    """
    responses.add(responses.POST, 'https://nourl/networks', json=network)
    network = tvm.networks.create(network['name'])
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


@responses.activate
def test_networks_delete_success(tvm, network):
    """
    test to delete network.
    """
    responses.add(
        responses.DELETE, 'https://nourl/networks/58ac2d96-81aa-472c-a418-74fcc6082049'
    )
    tvm.networks.delete(network['uuid'])


@responses.activate
def test_networks_details_success(tvm, network):
    """
    test to get details of specified network.
    """
    responses.add(
        responses.GET,
        'https://nourl/networks/58ac2d96-81aa-472c-a418-74fcc6082049',
        json={
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created': 1614777592524,
            'modified': 1614777727308,
            'scanner_count': 0,
            'uuid': '58ac2d96-81aa-472c-a418-74fcc6082049',
            'name': 'New Name',
            'description': '',
            'is_default': False,
            'created_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'modified_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'deleted': 1614777597698,
            'deleted_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created_in_seconds': 1614777592,
            'modified_in_seconds': 1614777727,
        },
    )
    resp = tvm.networks.details(network['uuid'])
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


def test_networks_edit_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.edit(str(uuid.uuid4()), 1)


def test_networks_edit_description_typeerror(tvm):
    """
    test to raise exception when type of description param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.edit(str(uuid.uuid4()), 'something', 1)


@responses.activate
def test_networks_edit_success(tvm, network):
    """
    test to update the specified network resource.
    """
    responses.add(
        responses.PUT,
        'https://nourl/networks/58ac2d96-81aa-472c-a418-74fcc6082049',
        json={
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created': 1614777592524,
            'modified': 1614786430959,
            'scanner_count': 0,
            'uuid': '58ac2d96-81aa-472c-a418-74fcc6082049',
            'name': 'New Name',
            'description': '',
            'is_default': False,
            'created_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'modified_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'deleted': 1614777597698,
            'deleted_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created_in_seconds': 1614777592,
            'modified_in_seconds': 1614786430,
        },
    )
    resp = tvm.networks.edit(network['uuid'], 'New Name - {}'.format(uuid.uuid4()))
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


@responses.activate
def test_networks_list_scanners_success(tvm):
    """
    test to get list of scanners associated to given network.
    """
    responses.add(
        responses.GET,
        'https://nourl/networks/00000000-0000-0000-0000-000000000000/scanners',
        json=NETWORKS_SCANNERS,
    )
    scanners = tvm.networks.list_scanners('00000000-0000-0000-0000-000000000000')
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


@responses.activate
def test_networks_unassigned_scanners_success(tvm, network):
    """
    test to get the list of scanners that are currently unassigned to the given network
    """
    responses.add(
        responses.GET,
        'https://nourl/networks/58ac2d96-81aa-472c-a418-74fcc6082049/assignable-scanners',
        json={
            'scanners': [
                {
                    'creation_date': 1614599787,
                    'group': True,
                    'id': 314909,
                    'key': 'af405ffce0b97ec47da5aaed7b3e3d9ceb59411630e2d6e18da1866874573b2a',
                    'last_connect': None,
                    'last_modification_date': 1614599787,
                    'linked': 1,
                    'name': 'US Cloud Scanner',
                    'num_scans': 0,
                    'owner': 'system',
                    'owner_id': 2201486,
                    'owner_name': 'system',
                    'owner_uuid': 'e2302807-7a65-4ad4-908a-5e8b8c9965e6',
                    'pool': True,
                    'scan_count': 0,
                    'source': 'service',
                    'status': 'on',
                    'timestamp': 1614599787,
                    'type': 'local',
                    'uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                    'supports_remote_logs': False,
                }
            ]
        },
    )
    scanners = tvm.networks.unassigned_scanners(network['uuid'])
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


@responses.activate
def test_networks_assign_scanners_success(tvm, network):
    """
    test to assign scanners to network.
    """
    responses.add(
        responses.GET,
        'https://nourl/networks/00000000-0000-0000-0000-000000000000/scanners',
        json=NETWORKS_SCANNERS,
    )
    responses.add(
        responses.POST,
        'https://nourl/networks/58ac2d96-81aa-472c-a418-74fcc6082049/scanners/c0317d83-342c-41ef-b7cc-ac7411d23eda',
    )
    scanner = tvm.networks.list_scanners('00000000-0000-0000-0000-000000000000')[0]
    tvm.networks.assign_scanners(network['uuid'], scanner['uuid'])


def test_networks_list_offset_typeerror(tvm):
    """
    test to raise exception when type of offset param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(offset='nope')


def test_networks_list_limit_typeerror(tvm):
    """
    test to raise exception when type of limit param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(limit='nope')


def test_networks_list_sort_field_typeerror(tvm):
    """
    test to raise exception when type of sort field param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(sort=((1, 'asc'),))


def test_networks_list_sort_direction_typeerror(tvm):
    """
    test to raise exception when type of sort direction param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(sort=(('uuid', 1),))


def test_networks_list_sort_direction_unexpectedvalue(tvm):
    """
    test to raise exception when value of sort direction param does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.networks.list(sort=(('uuid', 'nope'),))


def test_networks_list_filter_name_typeerror(tvm):
    """
    test to raise exception when type of filter_name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list((1, 'match', 'win'))


def test_networks_list_filter_operator_typeerror(tvm):
    """
    test to raise exception when type of filter_operator param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(('name', 1, 'win'))


def test_networks_list_filter_value_typeerror(tvm):
    """
    test to raise exception when type of filter_value param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(('name', 'match', 1))


def test_networks_list_filter_type_typeerror(tvm):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(filter_type=1)


def test_networks_list_wildcard_typeerror(tvm):
    """
    test to raise exception when type of wildcard param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(wildcard=1)


def test_networks_list_wildcard_fields_typeerror(tvm):
    """
    test to raise exception when type of wildcard_fields param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(wildcard_fields='nope')


def test_networks_list_include_deleted_typeerror(tvm):
    """
    test to raise exception when type of include_deleted param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.networks.list(include_deleted='nope')


@responses.activate
def test_networks_list(tvm):
    """
    test to get list of configured networks.
    """
    responses.add(
        responses.GET,
        'https://nourl/networks',
        json={
            'networks': [
                {
                    'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
                    'created': 1544743910953,
                    'modified': 1544743910953,
                    'scanner_count': 14,
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'name': 'Default',
                    'is_default': True,
                    'created_by': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
                    'modified_by': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
                    'created_in_seconds': 1544743910,
                    'modified_in_seconds': 1544743910,
                }
            ],
            'pagination': {
                'total': 1,
                'limit': 50,
                'offset': 0,
                'sort': [{'name': 'name', 'order': 'asc'}],
            },
        },
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '0'})],
    )
    count = 0
    networks = tvm.networks.list()
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


@responses.activate
def test_network_asset_count_network_num_days_invalidinputerror(tvm):
    """
    test to raise exception when value of num_days param is not valid.
    """
    responses.add(
        responses.GET,
        'https://nourl/networks/00000000-0000-0000-0000-000000000000/counts/assets-not-seen-in/-180',
        json={
            'statusCode': 400,
            'error': 'Bad Request',
            'message': 'child "days" fails because ["days" must be larger than or equal to 1]',
            'validation': {'source': 'params', 'keys': ['days']},
        },
        status=400,
    )
    with pytest.raises(BadRequestError):
        tvm.networks.network_asset_count('00000000-0000-0000-0000-000000000000', -180)


@responses.activate
def test_network_asset_count_network_success(tvm):
    """
    test to raise exception when type of network_id param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/networks/00000000-0000-0000-0000-000000000000/counts/assets-not-seen-in/180',
        json={'numAssetsTotal': 2, 'numAssetsNotSeen': 0},
    )
    network = '00000000-0000-0000-0000-000000000000'
    resp = tvm.networks.network_asset_count(network, 180)
    assert isinstance(resp, dict)
    check(resp, 'numAssetsTotal', int)
    check(resp, 'numAssetsNotSeen', int)


@responses.activate
def test_networks_assign_multiple_scanners_success(tvm, network, scanner):
    """
    test to pass multiple scanners
    """
    responses.add(
        responses.GET,
        'https://nourl/networks/00000000-0000-0000-0000-000000000000/scanners',
        json=NETWORKS_SCANNERS,
    )
    responses.add(
        responses.POST,
        'https://nourl/networks/58ac2d96-81aa-472c-a418-74fcc6082049/scanners',
    )
    scanner = tvm.networks.list_scanners('00000000-0000-0000-0000-000000000000')[0]
    tvm.networks.assign_scanners(network['uuid'], scanner['uuid'], scanner['uuid'])


def test_networks_unexpectedvalueerror(tvm, network):
    """
    test to raise exception when scanner_uuids are not passed

    """
    with pytest.raises(UnexpectedValueError):
        tvm.networks.assign_scanners(network['uuid'])


@responses.activate
def test_networks_list_fileds(tvm):
    """
    test to get list of configured networks.
    """
    responses.add(
        responses.GET,
        'https://nourl/networks',
        json={
            'networks': [],
            'pagination': {
                'total': 3,
                'limit': 50,
                'offset': 2,
                'sort': [{'name': 'name', 'order': 'asc'}],
            },
        },
        match=[
            matchers.query_param_matcher(
                {
                    'ft': 'or',
                    'w': 'match',
                    'wf': 'name',
                    'includeDeleted': 'True',
                    'limit': '50',
                    'offset': '2',
                }
            )
        ],
    )
    count = 0
    networks = tvm.networks.list(
        filter_type='or',
        include_deleted=True,
        offset=2,
        limit=50,
        wildcard='match',
        wildcard_fields=['name'],
    )
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


def test_network_create_assets_ttl_days_typeerror(tvm):
    with pytest.raises(TypeError):
        tvm.networks.create(
            'New Name - {}'.format(uuid.uuid4()), 'something', 'something'
        )


@responses.activate
def test_network_create_assets_ttl_days_invalid_input_error(tvm):
    responses.add(
        responses.POST,
        'https://nourl/networks',
        json={'error': 'Invalid TTL. When declared, a TTL must be at or above 90'},
        status=400,
    )
    with pytest.raises(BadRequestError):
        tvm.networks.create('New Name - {}'.format(uuid.uuid4()), 'something', -5)


@responses.activate
def test_network_edit_assets_ttl_days_type_error(tvm):
    responses.add(
        responses.POST,
        'https://nourl/networks',
        json={
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created': 1625575483559,
            'modified': 1625575483559,
            'scanner_count': 0,
            'uuid': '77264b5a-501b-4fd3-96e9-8b8b14e24f5f',
            'name': 'Network-a503b6aa-a962-4f6f-bd72-ebe59a2a0313',
            'description': '',
            'is_default': False,
            'created_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'modified_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created_in_seconds': 1625575483,
            'modified_in_seconds': 1625575483,
        },
    )
    with pytest.raises(TypeError):
        network = tvm.networks.create('Network-{}'.format(uuid.uuid4()))
        tvm.networks.edit(
            network_id=network['uuid'],
            name='New Name - {}'.format(uuid.uuid4()),
            assets_ttl_days='something',
        )


@responses.activate
def test_network_edit_assets_ttl_days_invalid_input_error(tvm):
    responses.add(
        responses.POST,
        'https://nourl/networks',
        json={
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created': 1625575492189,
            'modified': 1625575492189,
            'scanner_count': 0,
            'uuid': '6e7b8a63-2589-4c24-91a8-3f213955ec0f',
            'name': 'Network-686b14a3-dc9e-4d11-89a0-93c9b32a0c4b',
            'description': '',
            'is_default': False,
            'created_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'modified_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'created_in_seconds': 1625575492,
            'modified_in_seconds': 1625575492,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/networks/6e7b8a63-2589-4c24-91a8-3f213955ec0f',
        json={'error': 'Invalid TTL. When declared, a TTL must be at or above 90'},
        status=400,
    )
    with pytest.raises(BadRequestError):
        network = tvm.networks.create('Network-{}'.format(uuid.uuid4()))
        tvm.networks.edit(
            network_id=network['uuid'], name='something', assets_ttl_days=-5
        )
