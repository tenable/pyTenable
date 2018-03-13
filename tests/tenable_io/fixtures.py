import pytest, os
from tenable.tenable_io import TenableIO

@pytest.fixture(scope='session', autouse=True)
def api():
    return TenableIO(
        os.environ['TIO_TEST_ADMIN_ACCESS'], os.environ['TIO_TEST_ADMIN_SECRET'])

@pytest.fixture(scope='session', autouse=True)
def stdapi():
    return TenableIO(
        os.environ['TIO_TEST_STD_ACCESS'], os.environ['TIO_TEST_STD_SECRET'])