import pytest
from ..checker import check
from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception


@pytest.fixture
def zone(request, admin, vcr):
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


def test_scan_zones_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_zones._constructor(name=1)


def test_scan_zones_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_zones._constructor(description=1)


def test_scan_zones_constructor_ips_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_zones._constructor(ips=1)


def test_scan_zones_constructor_ips_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_zones._constructor(ips=[1])


def test_scan_zones_constructor_scanner_ids_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_zones._constructor(scanner_ids=1)


def test_scan_zones_constructor_scanner_ids_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_zones._constructor(scanner_ids=['not me'])


def test_scan_zones_constructor_success(sc):
    resp = sc.scan_zones._constructor(
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
    with pytest.raises(TypeError):
        admin.scan_zones.details('one')


@pytest.mark.vcr()
def test_scan_zones_details_fields_typeerror(admin):
    with pytest.raises(TypeError):
        admin.scan_zones.details(1, fields=1)


@pytest.mark.vcr()
def test_scan_zones_details_fields_item_typeerror(admin):
    with pytest.raises(TypeError):
        admin.scan_zones.details(1, fields=[1])


@pytest.mark.vcr()
def test_scan_zones_details_success(admin, zone):
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
    for zone in admin.scan_zones.list(fields=['id', 'name', 'description']):
        assert isinstance(zone, dict)
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)


@pytest.mark.vcr()
def test_scan_zones_edit_id_typeerror(admin):
    with pytest.raises(TypeError):
        admin.scan_zones.edit('one')


@pytest.mark.vcr()
def test_scan_zones_edit_success(admin, zone):
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
    with pytest.raises(TypeError):
        admin.scan_zones.delete('one')


@pytest.mark.vcr()
def test_scan_zones_delete_success(admin, zone):
    admin.scan_zones.delete(int(zone['id']))
