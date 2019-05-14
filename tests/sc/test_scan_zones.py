from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.fixture
def zone(request, admin, vcr):
    with vcr.use_cassette('test_scan_zones_create_success'):
        zone = admin.scan_zones.create('Example',
            ips=['192.168.0.0/24'])
    def teardown():
        try:
            with vcr.use_cassette('test_scan_zones_delete_success'):
                admin.scan_zones.delete(int(zone['id']))
        except APIError:
            pass
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
        scanner_ids=[1,2,3])
    assert resp == {
        'name': 'Example',
        'description': 'Test123',
        'ipList': '192.168.0.0/24',
        'scanners': [{'id': 1}, {'id': 2}, {'id': 3}]
    }

@pytest.mark.vcr()
def test_scan_zones_create_success(admin, zone):
    assert isinstance(zone, dict)
    check(zone, 'id', str)
    check(zone, 'name', str)
    check(zone, 'description', str)
    check(zone, 'ipList', str)
    check(zone, 'createdTime', str)
    check(zone, 'modifiedTime', str)
    check(zone, 'scanners', list)
    for s in zone['scanners']:
        check(s, 'id', str)
        check(s, 'name', str)
        check(s, 'description', str)
        check(s, 'status', str)
    check(zone, 'organizations', list)
    for o in zone['organizations']:
        check(o, 'id', str)
        check(o, 'name', str)
        check(o, 'description', str)
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
    z = admin.scan_zones.details(int(zone['id']))
    assert isinstance(z, dict)
    check(z, 'id', str)
    check(z, 'name', str)
    check(z, 'description', str)
    check(z, 'ipList', str)
    check(z, 'createdTime', str)
    check(z, 'modifiedTime', str)
    check(z, 'scanners', list)
    for s in z['scanners']:
        check(s, 'id', str)
        check(s, 'name', str)
        check(s, 'description', str)
        check(s, 'status', str)
    check(z, 'organizations', list)
    for o in z['organizations']:
        check(o, 'id', str)
        check(o, 'name', str)
        check(o, 'description', str)
    check(z, 'activeScanners', int)
    check(z, 'totalScanners', int)

@pytest.mark.vcr()
def test_scan_zones_edit_id_typeerror(admin):
    with pytest.raises(TypeError):
        admin.scan_zones.edit('one')

@pytest.mark.vcr()
def test_scan_zones_edit_success(admin, zone):
    z = admin.scan_zones.edit(int(zone['id']), name='NewName')
    assert isinstance(z, dict)
    check(z, 'id', str)
    check(z, 'name', str)
    check(z, 'description', str)
    check(z, 'ipList', str)
    check(z, 'createdTime', str)
    check(z, 'modifiedTime', str)
    check(z, 'scanners', list)
    for s in z['scanners']:
        check(s, 'id', str)
        check(s, 'name', str)
        check(s, 'description', str)
        check(s, 'status', str)
    check(z, 'organizations', list)
    for o in z['organizations']:
        check(o, 'id', str)
        check(o, 'name', str)
        check(o, 'description', str)
    check(z, 'activeScanners', int)
    check(z, 'totalScanners', int)

@pytest.mark.vcr()
def test_scan_zones_delete_id_typeerror(admin):
    with pytest.raises(TypeError):
        admin.scan_zones.delete('one')

@pytest.mark.vcr()
def test_scan_zones_delete_success(admin, zone):
    admin.scan_zones.delete(int(zone['id']))