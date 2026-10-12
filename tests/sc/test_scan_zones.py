"""
test file for testing various scenarios in security center's scan zones functionality
"""

import pytest
import responses
from responses import matchers

from ..checker import check


@pytest.fixture
def zone():
    """
    test fixture for zone
    """
    return {
        'id': '2',
        'name': 'Example',
        'description': '',
        'ipList': '192.168.0.0/24',
        'createdTime': '1553205832',
        'modifiedTime': '1553205832',
        'scanners': [],
        'organizations': [],
        'activeScanners': 0,
        'totalScanners': 0,
    }


def test_scan_zones_constructor_name_typeerror(tsc):
    """
    test scan zones constructor for name type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones._constructor(name=1)


def test_scan_zones_constructor_description_typeerror(tsc):
    """
    test scan zones constructor for description type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones._constructor(description=1)


def test_scan_zones_constructor_ips_typeerror(tsc):
    """
    test scan zones constructor for ips type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones._constructor(ips=1)


def test_scan_zones_constructor_ips_item_typeerror(tsc):
    """
    test scan zones constructor for 'ips item' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones._constructor(ips=[1])


def test_scan_zones_constructor_scanner_ids_typeerror(tsc):
    """
    test scan zones constructor for 'scanner ids' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones._constructor(scanner_ids=1)


def test_scan_zones_constructor_scanner_ids_item_typeerror(tsc):
    """
    test scan zones constructor for 'scanner ids item' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones._constructor(scanner_ids=['not me'])


def test_scan_zones_constructor_success(tsc):
    """
    test scan zones constructor for success
    """
    resp = tsc.scan_zones._constructor(
        name='Example',
        description='Test123',
        ips=['192.168.0.0/24'],
        scanner_ids=[1, 2, 3],
    )
    assert resp == {
        'name': 'Example',
        'description': 'Test123',
        'ipList': '192.168.0.0/24',
        'scanners': [{'id': 1}, {'id': 2}, {'id': 3}],
    }


@responses.activate
def test_scan_zones_create_success(tsc):
    """
    test scan zones create for success
    """
    responses.post(
        'https://nourl/rest/zone',
        json={
            'type': 'regular',
            'response': {
                'id': '2',
                'name': 'Example',
                'description': '',
                'ipList': '192.168.0.0/24',
                'createdTime': '1553205832',
                'modifiedTime': '1553205832',
                'scanners': [],
                'organizations': [],
                'activeScanners': 0,
                'totalScanners': 0,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553205832,
        },
    )
    zone = tsc.scan_zones.create('Example', ips=['192.168.0.0/24'])
    assert isinstance(zone, dict)
    check(zone, 'id', str)
    check(zone, 'name', str)
    check(zone, 'description', str)
    check(zone, 'ipList', str)
    check(zone, 'createdTime', str)
    check(zone, 'modifiedTime', str)
    check(zone, 'scanners', list)
    for scanner in zone['scanners']:
        check(scanner, 'id', str)
        check(scanner, 'name', str)
        check(scanner, 'description', str)
        check(scanner, 'status', str)
    check(zone, 'organizations', list)
    for organization in zone['organizations']:
        check(organization, 'id', str)
        check(organization, 'name', str)
        check(organization, 'description', str)
    check(zone, 'activeScanners', int)
    check(zone, 'totalScanners', int)


def test_scan_zones_details_id_typeerror(tsc):
    """
    test scan zones details for id type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones.details('one')


def test_scan_zones_details_fields_typeerror(tsc):
    """
    test scan zones details for fields type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones.details(1, fields=1)


def test_scan_zones_details_fields_item_typeerror(tsc):
    """
    test scan zones details for 'fields item' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones.details(1, fields=[1])


@responses.activate
def test_scan_zones_details_success(tsc, zone):
    """
    test scan zones details for success
    """
    responses.get(
        'https://nourl/rest/zone/2',
        json={
            'type': 'regular',
            'response': {
                'id': '7',
                'name': 'Example',
                'description': '',
                'ipList': '192.168.0.0/24',
                'createdTime': '1553205885',
                'modifiedTime': '1553205885',
                'scanners': [],
                'organizations': [],
                'activeScanners': 0,
                'totalScanners': 0,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553205885,
        },
    )
    zone = tsc.scan_zones.details(int(zone['id']))
    assert isinstance(zone, dict)
    check(zone, 'id', str)
    check(zone, 'name', str)
    check(zone, 'description', str)
    check(zone, 'ipList', str)
    check(zone, 'createdTime', str)
    check(zone, 'modifiedTime', str)
    check(zone, 'scanners', list)
    for scanner in zone['scanners']:
        check(scanner, 'id', str)
        check(scanner, 'name', str)
        check(scanner, 'description', str)
        check(scanner, 'status', str)
    check(zone, 'organizations', list)
    for organization in zone['organizations']:
        check(organization, 'id', str)
        check(organization, 'name', str)
        check(organization, 'description', str)
    check(zone, 'activeScanners', int)
    check(zone, 'totalScanners', int)


@responses.activate
def test_scan_zones_list_success(tsc):
    """
    test scan zones list for success
    """
    responses.get(
        'https://nourl/rest/zone',
        json={
            'type': 'regular',
            'response': [
                {'id': '7', 'name': 'Example', 'description': ''},
                {'id': '8', 'name': 'Example', 'description': ''},
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553205885,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    for zone in tsc.scan_zones.list(fields=['id', 'name', 'description']):
        assert isinstance(zone, dict)
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)


def test_scan_zones_edit_id_typeerror(tsc):
    """
    test scan zones edit for id type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones.edit('one')


@responses.activate
def test_scan_zones_edit_success(tsc, zone):
    """
    test scan zones edit for success
    """
    responses.patch(
        'https://nourl/rest/zone/2',
        json={
            'type': 'regular',
            'response': {
                'id': '8',
                'name': 'NewName',
                'description': '',
                'ipList': '192.168.0.0/24',
                'createdTime': '1553205886',
                'modifiedTime': '1553205886',
                'scanners': [],
                'organizations': [],
                'activeScanners': 0,
                'totalScanners': 0,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553205886,
        },
    )
    zone = tsc.scan_zones.edit(int(zone['id']), name='NewName')
    assert isinstance(zone, dict)
    check(zone, 'id', str)
    check(zone, 'name', str)
    check(zone, 'description', str)
    check(zone, 'ipList', str)
    check(zone, 'createdTime', str)
    check(zone, 'modifiedTime', str)
    check(zone, 'scanners', list)
    for scanner in zone['scanners']:
        check(scanner, 'id', str)
        check(scanner, 'name', str)
        check(scanner, 'description', str)
        check(scanner, 'status', str)
    check(zone, 'organizations', list)
    for organization in zone['organizations']:
        check(organization, 'id', str)
        check(organization, 'name', str)
        check(organization, 'description', str)
    check(zone, 'activeScanners', int)
    check(zone, 'totalScanners', int)


def test_scan_zones_delete_id_typeerror(tsc):
    """
    test scan zones delete for id type error
    """
    with pytest.raises(TypeError):
        tsc.scan_zones.delete('one')


@responses.activate
def test_scan_zones_delete_success(tsc, zone):
    """
    test scan zones delete for success
    """
    responses.delete(
        'https://nourl/rest/zone/2',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553205832,
        },
    )
    tsc.scan_zones.delete(int(zone['id']))
