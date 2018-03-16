import pytest, os, uuid
from tenable.tenable_io import TenableIO
from tenable.errors import *

@pytest.fixture(scope='session', autouse=True)
def api():
    return TenableIO(
        os.environ['TIO_TEST_ADMIN_ACCESS'], os.environ['TIO_TEST_ADMIN_SECRET'])

@pytest.fixture(scope='session', autouse=True)
def stdapi():
    return TenableIO(
        os.environ['TIO_TEST_STD_ACCESS'], os.environ['TIO_TEST_STD_SECRET'])

@pytest.fixture
def agent(request, api):
    return api.agents.list().next()

@pytest.fixture
def folder(request, api):
    folder = api.folders.create(str(uuid.uuid4())[:20])
    def teardown():
        try:
            api.folders.delete(folder)
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return folder