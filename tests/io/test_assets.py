'''
test assets
'''
import time
import uuid
import pytest
from tenable.errors import UnexpectedValueError, PermissionError
from tests.checker import check, single
from tests.io.test_networks import fixture_network

@pytest.mark.vcr()
def test_assets_list(api):
    '''
    test to get list of assets
    '''
    assets = api.assets.list()
    assert isinstance(assets, list)
    resp = assets[0]
    check(resp, 'aws_ec2_name', list)
    check(resp, 'fqdn', list)
    check(resp, 'has_agent', bool)
    check(resp, 'id', 'uuid')
    check(resp, 'ipv4', list)
    check(resp, 'ipv6', list)
    check(resp, 'last_seen', 'datetime')
    check(resp, 'mac_address', list)
    check(resp, 'netbios_name', list)
    check(resp, 'operating_system', list)
    check(resp, 'sources', list)
    for source in resp['sources']:
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')
        check(source, 'name', str)

@pytest.mark.vcr()
def test_assets_import_assets_typeerror(api):
    '''
    test to raise exception when type of assets param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.assets.asset_import('pytest', 1)

@pytest.mark.vcr()
def test_assets_import_source_typeerror(api):
    '''
    test to raise exception when type of source param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.assets.asset_import(1, {
            'fqdn': ['example.py.test'],
            'ipv4': ['192.168.254.1'],
            'netbios_name': '',
            'mac_address': []
        })

@pytest.mark.vcr()
def test_assets_import_standard_user_permissionerror(stdapi):
    '''
    test to raise exception when standard user try to import asset.
    '''
    with pytest.raises(PermissionError):
        stdapi.assets.asset_import( 'pytest', {
            'fqdn': ['example.py.test'],
            'ipv4': ['192.168.254.1'],
            'netbios_name': '',
            'mac_address': []
        })

@pytest.mark.vcr()
def test_assets_import(api):
    '''
    test to import asset
    '''
    resp = api.assets.asset_import('pytest', {
        'fqdn': ['example.py.test'],
        'ipv4': ['192.168.254.1'],
        'netbios_name': '',
        'mac_address': []
    })
    single(resp, 'uuid')

@pytest.mark.vcr()
def test_assets_import_jobs(api):
    '''
    test to get list of asset import jobs
    '''
    jobs = api.assets.list_import_jobs()
    assert isinstance(jobs, list)
    for i in jobs:
        check(i, 'batches', int)
        check(i, 'container_id', 'uuid')
        check(i, 'end_time', int)
        check(i, 'failed_assets', int)
        check(i, 'job_id', 'uuid')
        check(i, 'last_update_time', int)
        check(i, 'source', str)
        check(i, 'start_time', int)
        check(i, 'status', str)
        check(i, 'status_message', str)
        check(i, 'uploaded_assets', int)

@pytest.mark.vcr()
def test_assets_import_job_info(api):
    '''
    test to get the details about a specific asset import job
    '''
    jobs = api.assets.list_import_jobs()
    if len(jobs) > 0:
        job = api.assets.import_job_details(jobs[0]['job_id'])
        check(job, 'batches', int)
        check(job, 'container_id', 'uuid')
        check(job, 'end_time', int)
        check(job, 'failed_assets', int)
        check(job, 'job_id', 'uuid')
        check(job, 'last_update_time', int)
        check(job, 'source', str)
        check(job, 'start_time', int)
        check(job, 'status', str)
        check(job, 'status_message', str)
        check(job, 'uploaded_assets', int)
        assert job['job_id'] == jobs[0]['job_id']

@pytest.mark.vcr()
def test_assets_tags_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.assets.tags(1)

@pytest.mark.vcr()
def test_assets_tags_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.assets.tags('somethign else')

@pytest.mark.vcr()
def test_workbenches_asset_delete_asset_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_delete(1)

@pytest.mark.vcr()
def test_workbenches_asset_delete_success(api):
    '''
    test to delete the asset
    '''
    asset = api.workbenches.assets()[0]
    api.workbenches.asset_delete(asset['id'])

@pytest.mark.vcr()
def test_assign_tags(api):
    '''
    test to raise exception when action param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.assets.assign_tags('foo', [], [])

@pytest.mark.vcr()
def test_assets_move_assets_source_typeerror(api):
    '''
    test to raise exception when type of source param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.assets.move_assets(1, str(uuid.uuid4()), ["127.0.0.1"])

@pytest.mark.vcr()
def test_assets_move_assets_source_unexpectedvalueerror(api):
    '''
    test to raise exception when source param value does not match the pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.assets.move_assets('nope', str(uuid.uuid4()), ["127.0.0.1"])

@pytest.mark.vcr()
def test_assets_move_assets_destination_typeerror(api):
    '''
    test to raise exception when type of destination param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.assets.move_assets(str(uuid.uuid4()), 1, ["127.0.0.1"])

@pytest.mark.vcr()
def test_assets_move_assets_destination_unexpectedvalueerror(api):
    '''
    test to raise exception when destination param value does not match the pattern.
    '''
    with pytest.raises(UnexpectedValueError):
        api.assets.move_assets(str(uuid.uuid4()), 'nope', ["127.0.0.1"])

@pytest.mark.vcr()
def test_assets_move_assets_target_typeerror(api):
    '''
    test to raise exception when type of target param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.assets.move_assets(str(uuid.uuid4()), str(uuid.uuid4()), 1)

@pytest.mark.vcr()
def test_assets_move_assets_success(api, network):
    '''
    test to move assets from the specified network to another network
    '''
    api.assets.asset_import('pytest', {
        'fqdn': ['example.py.test'],
        'ipv4': ['192.168.254.1'],
        'netbios_name': '',
        'mac_address': []
    })
    time.sleep(15)
    resp = api.assets.move_assets(
        '00000000-0000-0000-0000-000000000000', network['uuid'], ['192.168.254.1'])
    check(resp['response']['data'], 'asset_count', int)
    assert resp['response']['data']['asset_count'] == 1

def test_assets_bulk_delete_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.assets.bulk_delete(filter_type=1)

@pytest.mark.vcr()
def test_assets_bulk_delete_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.assets.bulk_delete(filter_type='NOT')

@pytest.mark.vcr()
def test_assets_bulk_delete_bad_filter(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.assets.bulk_delete(('operating_system', 'contains', 'Linux'))

@pytest.mark.vcr()
def test_assets_bulk_delete_success(api):
    '''
    test to delete multiple assets
    '''
    api.assets.asset_import('pytest', {
        'fqdn': ['example1.py.test'],
        'ipv4': ['192.168.254.1'],
        'netbios_name': '',
        'mac_address': []
    })
    api.assets.asset_import('pytest', {
        'fqdn': ['example2.py.test'],
        'ipv4': ['192.168.254.1'],
        'netbios_name': '',
        'mac_address': []
    })
    time.sleep(5)
    resp = api.assets.bulk_delete(('ipv4', 'eq', '192.168.254.1'))
    check(resp['response']['data'], 'asset_count', int)
    assert resp['response']['data']['asset_count'] == 2
