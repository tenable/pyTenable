import pytest, os, uuid
from tenable.cs import ContainerSecurity
from tenable.errors import *
from tests.checker import check

@pytest.fixture(autouse=True)
def api():
    return ContainerSecurity(
        os.environ['TIO_TEST_ADMIN_ACCESS'], os.environ['TIO_TEST_ADMIN_SECRET'])

@pytest.fixture(autouse=True)
def stdapi():
    return ContainerSecurity(
        os.environ['TIO_TEST_STD_ACCESS'], os.environ['TIO_TEST_STD_SECRET'])

@pytest.fixture
def image_id(request, api):
    import docker
    client = docker.from_env()
    image = client.images.pull('alpine', tag='3.1')
    iid = api.uploads.docker_push('alpine', tag='3.1')
    return iid

@pytest.fixture
def import_id(request, api):
    resp = api.imports.create(
        host='registry.hub.docker.com',
        port=443,
        username='someone',
        password='secret_squirrel',
        provider='dr',
    )
    def teardown():
        try:
            api.imports.delete(resp['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return resp['id']