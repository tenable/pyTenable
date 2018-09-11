import pytest, os, uuid
from tenable.container_security import ContainerSecurity
from tenable.errors import *

@pytest.fixture(autouse=True)
def api():
    return TenableIO(
        os.environ['TIO_TEST_ADMIN_ACCESS'], os.environ['TIO_TEST_ADMIN_SECRET'])

@pytest.fixture(autouse=True)
def stdapi():
    return TenableIO(
        os.environ['TIO_TEST_STD_ACCESS'], os.environ['TIO_TEST_STD_SECRET'])

