'''conftest'''
import os
import pytest
from tenable.cs import ContainerSecurity
from tests.pytenable_log_handler import setup_logging_to_file


@pytest.fixture(scope='module')
def vcr_config():
    '''vcr config fixture'''
    return {
        'filter_headers': [
            ('X-APIKeys', 'accessKey=TIO_ACCESS_KEY;secretKey=TIO_SECRET_KEY'),
            ('x-request-uuid', 'ffffffffffffffffffffffffffffffff'),
        ],
    }


@pytest.fixture(autouse=True)
def api():
    '''api keys fixture'''
    setup_logging_to_file()
    return ContainerSecurity(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')


@pytest.fixture(autouse=True)
def stdapi():
    '''std api keys fixture'''
    return ContainerSecurity(
        os.getenv('TIO_TEST_STD_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_STD_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')


@pytest.fixture
def image_id(api):
    '''fixture to return image_id'''
    iid = api.uploads.docker_push('alpine', tag='3.1')
    return iid
