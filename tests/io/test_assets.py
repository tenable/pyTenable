from .fixtures import *
from tenable.errors import *

def test_list(api):
    assert isinstance(api.assets.list(), list)

def test_import_assets_typeerror(api):
    with pytest.raises(TypeError):
        api.assets.asset_import(1, 'pytest')

def test_import_source_typeerror(api):
    with pytest.raises(TypeError):
        api.assets.asset_import([{
            'fqdn': ['example.py.test'], 
            'ipv4': ['192.168.254.1'], 
            'netbios_name': '', 
            'mac_address': []
        }], 1)

def test_import_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.assets.asset_import([{
            'fqdn': ['example.py.test'], 
            'ipv4': ['192.168.254.1'], 
            'netbios_name': '', 
            'mac_address': []
        }], 'pytest')   

def test_import(api):
    resp = api.assets.asset_import([{
        'fqdn': ['example.py.test'], 
        'ipv4': ['192.168.254.1'], 
        'netbios_name': '', 
        'mac_address': []
    }], 'pytest')
    single(resp, 'uuid')

def test_import_jobs(api):
    jobs = api.assets.import_jobs()
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

def test_import_job_info(api):
    jobs = api.assets.import_jobs()
    if len(jobs) > 0:
        job = api.assets.import_job_info(jobs[0]['job_id'])
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