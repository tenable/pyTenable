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
@pytest.mark.skip('We don\'t want to actually delete an asset')
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
@pytest.mark.xfail(raises=AssertionError, reason="asset import job not completed")
def test_assets_move_assets_success(api, network):
    '''
    test to move assets from the specified network to another network
    '''
    ip_addr = '192.168.254.1'

    # import asset
    job_id = api.assets.asset_import('pytest', {
        'fqdn': ['example.py.test'],
        'ipv4': [ip_addr],
        'netbios_name': '',
        'mac_address': []
    })

    # wait for asset to import
    iterate = True
    iterate_count = 0
    while iterate:
        time.sleep(5)
        job = api.assets.list_import_jobs()
        asset = [data['status'] for data in job
                 if job_id in data['job_id']]
        iterate_count = iterate_count + 1

        # break iteration
        if iterate_count == 5 or (len(asset) == 1 and asset[0] == 'COMPLETE') :
            break

    # move asset to new network
    time.sleep(45)
    resp = api.assets.move_assets(
        '00000000-0000-0000-0000-000000000000', network['uuid'], ['192.168.254.1'])

    # remove imported asset
    api.assets.bulk_delete(('ipv4', 'eq', ip_addr))

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
@pytest.mark.xfail(raises=AssertionError, reason="asset import job not completed")
def test_assets_bulk_delete_success(api):
    '''
    test to delete multiple assets
    '''
    ip_addr = '192.168.254.2'

    # import assets
    first_asset = api.assets.asset_import('pytest', {
        'fqdn': ['example1.py.test'],
        'ipv4': [ip_addr],
        'netbios_name': '',
        'mac_address': []
    })
    second_asset = api.assets.asset_import('pytest', {
        'fqdn': ['example2.py.test'],
        'ipv4': [ip_addr],
        'netbios_name': '',
        'mac_address': []
    })

    # wait for asset to import
    iterate = True
    iterate_count = 0
    while iterate:
        time.sleep(5)
        job = api.assets.list_import_jobs()
        asset = [data['status'] for data in job
                 if first_asset in data['job_id'] or second_asset in data['job_id']]
        iterate_count = iterate_count + 1

        # break iteration
        if iterate_count == 5 or (
                len(asset) == 2 and len(set(asset)) == 1 and asset[0] == 'COMPLETE'):
            break

    # remove imported asset
    time.sleep(45)
    resp = api.assets.bulk_delete(('ipv4', 'eq', ip_addr))
    check(resp['response']['data'], 'asset_count', int)
    assert resp['response']['data']['asset_count'] == 2


@pytest.mark.vcr()
def test_assets_details_success_fields(api):
    """
    test to check the details of the assets and their types
    """
    asset = api.assets.list()
    asset_id = [i.get('id') for i in asset][0]
    resp = api.assets.details(asset_id)
    assert isinstance(resp, dict)
    check(resp, 'id', 'uuid')
    check(resp, 'has_agent', bool)
    check(resp, 'created_at', 'datetime')
    check(resp, 'updated_at', 'datetime')
    check(resp, 'first_seen', 'datetime')
    check(resp, 'last_seen', 'datetime')
    check(resp, 'last_scan_target', str, allow_none=True)
    check(resp, 'last_authenticated_scan_date', 'datetime', allow_none=True)
    check(resp, 'last_licensed_scan_date', 'datetime', allow_none=True)
    check(resp, 'last_scan_id', str, allow_none=True)
    check(resp, 'last_schedule_id', str, allow_none=True)
    check(resp, 'sources', list)

    for source in resp['sources']:
        check(source, 'name', str)
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')

    check(resp, 'tags', list)

    for tag in resp['tags']:
        check(tag, 'tag_uuid', 'uuid')
        check(tag, 'tag_key', str)
        check(tag, 'tag_value', str)
        check(tag, 'added_by', 'uuid')
        check(tag, 'added_at', 'datetime')

    check(resp, 'acr_score', str, allow_none=True)
    check(resp, 'exposure_score', int, allow_none=True)
    check(resp, 'acr_drivers', str, allow_none=True)
    check(resp, 'scan_frequency', list, allow_none=True)
    check(resp, 'interfaces', list)

    for interface in resp['interfaces']:
        check(interface, 'name', str)
        check(interface, 'fqdn', list)
        check(interface, 'mac_address', list)
        check(interface, 'ipv4', list)
        check(interface, 'ipv6', list)

    check(resp, 'network_id', list)
    check(resp, 'ipv4', list)
    check(resp, 'ipv6', list)
    check(resp, 'fqdn', list)
    check(resp, 'mac_address', list)
    check(resp, 'netbios_name', list)
    check(resp, 'operating_system', list)
    check(resp, 'system_type', list)
    check(resp, 'tenable_uuid', list)
    check(resp, 'hostname', list)
    check(resp, 'agent_name', list)
    check(resp, 'bios_uuid', list)
    check(resp, 'gcp_zone', list)
    check(resp, 'gcp_project_id', list)
    check(resp, 'azure_resource_id', list)
    check(resp, 'azure_vm_id', list)
    check(resp, 'aws_ec2_name', list)
    check(resp, 'aws_ec2_product_code', list)
    check(resp, 'aws_subnet_id', list)
    check(resp, 'aws_ec2_instance_type', list)
    check(resp, 'aws_ec2_instance_state_name', list)
    check(resp, 'aws_ec2_instance_group_name', list)
    check(resp, 'aws_region', list)
    check(resp, 'aws_availability_zone', list)
    check(resp, 'aws_owner_id', list)
    check(resp, 'aws_ec2_instance_ami_id', list)
    check(resp, 'aws_ec2_instance_id', list)
    check(resp, 'bigfix_asset_id', list)
    check(resp, 'installed_software', list)
    check(resp, 'servicenow_sysid', list)
    check(resp, 'qualys_host_id', list)
    check(resp, 'qualys_asset_id', list)
    check(resp, 'mcafee_epo_agent_guid', list)
    check(resp, 'mcafee_epo_guid', list)
    check(resp, 'ssh_fingerprint', list)
    check(resp, 'gcp_instance_id', list)
    check(resp, 'security_protections', list)
    check(resp, 'exposure_confidence_value', float, allow_none=True)
