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
    api.assets.asset_import([{
        'fqdn': ['example.py.test'], 
        'ipv4': ['192.168.254.1'], 
        'netbios_name': '', 
        'mac_address': []
    }], 'pytest')

def test_import_jobs(api):
    jobs = api.assets.import_jobs()
    assert isinstance(jobs, list)

def test_import_job_info(api):
    jobs = api.assets.import_jobs()
    if len(jobs) > 0:
        job = api.assets.import_job_info(jobs[0]['job_id'])
        assert job['job_id'] == jobs[0]['job_id']