from .fixtures import *
from tenable.errors import *

def test_list(api):
    for i in api.jobs.list():
        check(i, 'container_id', str)
        check(i, 'job_id', str)
        check(i, 'error', str)
        check(i, 'job_status', str)
        check(i, 'created_at', 'datetime')
        check(i, 'updated_at', 'datetime')

def test_status_job_id_typeerror(api):
    with pytest.raises(TypeError):
        api.jobs.status(job_id='12345')

def test_status_image_id_typeerror(api):
    with pytest.raises(TypeError):
        api.jobs.status(image_id=1234)

def test_status_digest_typeerror(api):
    with pytest.raises(TypeError):
        api.jobs.status(digest=12345)

def test_status_image_id(api, image_id):
    status = api.jobs.status(image_id=image_id)
    assert isinstance(status, dict)
    check(status, 'job_status', str)
    check(status, 'job_id', str)
    check(status, 'created_at', 'datetime')
    check(status, 'container_id', str)
    check(status, 'updated_at', 'datetime')
    check(status, 'error', str)
    check(status, 'digest', str)

def test_status_digest(api, image_id):
    job = api.jobs.status(image_id=image_id)
    status = api.jobs.status(digest=job['digest'])
    assert isinstance(status, dict)
    check(status, 'job_status', str)
    check(status, 'job_id', str)
    check(status, 'created_at', 'datetime')
    check(status, 'container_id', str)
    check(status, 'updated_at', 'datetime')
    check(status, 'error', str)
    check(status, 'digest', str)

@pytest.mark.skip(reason="This call isn't working as expected.")
def test_status_job_id(api, image_id):
    job = api.jobs.status(image_id=image_id)
    status = api.jobs.status(job_id=job['job_id'])
    assert isinstance(status, dict)
    check(status, 'job_status', str)
    check(status, 'job_id', str)
    check(status, 'created_at', 'datetime')
    check(status, 'container_id', str)
    check(status, 'updated_at', 'datetime')
    check(status, 'error', str)
    check(status, 'digest', str)