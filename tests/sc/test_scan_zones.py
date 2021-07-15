'''
test file for testing various scenarios in security center's scan zones functionality
'''
import pytest

from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception
from ..checker import check


@pytest.fixture
def zone(request, admin, vcr):
    '''
    test fixture for zone
    '''
    with vcr.use_cassette('test_scan_zones_create_success'):
        zone = admin.scan_zones.create('Example',
                                       ips=['192.168.0.0/24'])

    def teardown():
        try:
            with vcr.use_cassette('test_scan_zones_delete_success'):
                admin.scan_zones.delete(int(zone['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return zone


def test_scan_zones_constructor_name_typeerror(security_center):
    '''
    test scan zones constructor for name type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_zones._constructor(name=1)


def test_scan_zones_constructor_description_typeerror(security_center):
    '''
    test scan zones constructor for description type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_zones._constructor(description=1)


def test_scan_zones_constructor_ips_typeerror(security_center):
    '''
    test scan zones constructor for ips type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_zones._constructor(ips=1)


def test_scan_zones_constructor_ips_item_typeerror(security_center):
    '''
    test scan zones constructor for 'ips item' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_zones._constructor(ips=[1])


def test_scan_zones_constructor_scanner_ids_typeerror(security_center):
    '''
    test scan zones constructor for 'scanner ids' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_zones._constructor(scanner_ids=1)


def test_scan_zones_constructor_scanner_ids_item_typeerror(security_center):
    '''
    test scan zones constructor for 'scanner ids item' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_zones._constructor(scanner_ids=['not me'])


def test_scan_zones_constructor_success(security_center):
    '''
    test scan zones constructor for success
    '''
    resp = security_center.scan_zones._constructor(
        name='Example',
        description='Test123',
        ips=['192.168.0.0/24'],
        scanner_ids=[1, 2, 3])
    assert resp == {
        'name': 'Example',
        'description': 'Test123',
        'ipList': '192.168.0.0/24',
        'scanners': [{'id': 1}, {'id': 2}, {'id': 3}]
    }


@pytest.mark.vcr()
def test_scan_zones_create_success(zone):
    '''
    test scan zones create for success
    '''
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


@pytest.mark.vcr()
def test_scan_zones_details_id_typeerror(admin):
    '''
    test scan zones details for id type error
    '''
    with pytest.raises(TypeError):
        admin.scan_zones.details('one')


@pytest.mark.vcr()
def test_scan_zones_details_fields_typeerror(admin):
    '''
    test scan zones details for fields type error
    '''
    with pytest.raises(TypeError):
        admin.scan_zones.details(1, fields=1)


@pytest.mark.vcr()
def test_scan_zones_details_fields_item_typeerror(admin):
    '''
    test scan zones details for 'fields item' type error
    '''
    with pytest.raises(TypeError):
        admin.scan_zones.details(1, fields=[1])


@pytest.mark.vcr()
def test_scan_zones_details_success(admin, zone):
    '''
    test scan zones details for success
    '''
    zone = admin.scan_zones.details(int(zone['id']))
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


@pytest.mark.vcr()
def test_scan_zones_list_success(admin):
    '''
    test scan zones list for success
    '''
    for zone in admin.scan_zones.list(fields=['id', 'name', 'description']):
        assert isinstance(zone, dict)
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)


@pytest.mark.vcr()
def test_scan_zones_edit_id_typeerror(admin):
    '''
    test scan zones edit for id type error
    '''
    with pytest.raises(TypeError):
        admin.scan_zones.edit('one')


@pytest.mark.vcr()
def test_scan_zones_edit_success(admin, zone):
    '''
    test scan zones edit for success
    '''
    zone = admin.scan_zones.edit(int(zone['id']), name='NewName')
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


@pytest.mark.vcr()
def test_scan_zones_delete_id_typeerror(admin):
    '''
    test scan zones delete for id type error
    '''
    with pytest.raises(TypeError):
        admin.scan_zones.delete('one')


@pytest.mark.vcr()
def test_scan_zones_delete_success(admin, zone):
    '''
    test scan zones delete for success
    '''
    admin.scan_zones.delete(int(zone['id']))
