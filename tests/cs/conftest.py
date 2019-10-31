import pytest, os, uuid
from tenable.cs import ContainerSecurity
from tenable.errors import *
from tests.checker import check

@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_headers': [
            ('X-APIKeys', 'accessKey=TIO_ACCESS_KEY;secretKey=TIO_SECRET_KEY'),
            ('x-request-uuid', 'ffffffffffffffffffffffffffffffff'),
        ],
    }

@pytest.fixture(autouse=True)
def api():
    return ContainerSecurity(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')

@pytest.fixture(autouse=True)
def stdapi():
    return ContainerSecurity(
        os.getenv('TIO_TEST_STD_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_STD_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')

@pytest.fixture
def image_id(request, api):
    import docker
    client = docker.from_env()
    image = client.images.pull('alpine', tag='3.1')
    iid = api.uploads.docker_push('alpine', tag='3.1')
    return iid