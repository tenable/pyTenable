from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_assets_list(api):
    assets = api.assets.list()
    assert isinstance(assets, list)
    a = assets[0]
    check(a, 'aws_ec2_name', list)
    check(a, 'fqdn', list)
    check(a, 'has_agent', bool)
    check(a, 'id', 'uuid')
    check(a, 'ipv4', list)
    check(a, 'ipv6', list)
    check(a, 'last_seen', 'datetime')
    check(a, 'mac_address', list)
    check(a, 'netbios_name', list)
    check(a, 'operating_system', list)
    check(a, 'sources', list)
    for s in a['sources']:
        check(s, 'first_seen', 'datetime')
        check(s, 'last_seen', 'datetime')
        check(s, 'name', str)

@pytest.mark.vcr()
def test_assets_import_assets_typeerror(api):
    with pytest.raises(TypeError):
        api.assets.asset_import('pytest', 1)

@pytest.mark.vcr()
def test_assets_import_source_typeerror(api):
    with pytest.raises(TypeError):
        api.assets.asset_import(1, {
            'fqdn': ['example.py.test'],
            'ipv4': ['192.168.254.1'],
            'netbios_name': '',
            'mac_address': []
        })

@pytest.mark.vcr()
def test_assets_import_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.assets.asset_import( 'pytest', {
            'fqdn': ['example.py.test'],
            'ipv4': ['192.168.254.1'],
            'netbios_name': '',
            'mac_address': []
        })

@pytest.mark.vcr()
def test_assets_import(api):
    resp = api.assets.asset_import('pytest', {
        'fqdn': ['example.py.test'],
        'ipv4': ['192.168.254.1'],
        'netbios_name': '',
        'mac_address': []
    })
    single(resp, 'uuid')

@pytest.mark.vcr()
def test_assets_import_jobs(api):
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
    with pytest.raises(TypeError):
        api.assets.tags(1)

@pytest.mark.vcr()
def test_assets_tags_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.assets.tags('somethign else')

@pytest.mark.vcr()
def test_workbenches_asset_delete_asset_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_delete(1)

@pytest.mark.vcr()
def test_workbenches_asset_delete_success(api):
    asset = api.workbenches.assets()[0]
    api.workbenches.asset_delete(asset['id'])

@pytest.mark.vcr()
def test_assign_tags(api):
    with pytest.raises(UnexpectedValueError):
        api.assets.assign_tags('foo', [], [])
