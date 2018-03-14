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

@pytest.fixture
def agentgroup(request, api):
    group = api.agent_groups.create(str(uuid.uuid4()))
    def teardown():
        try:
            api.agent_groups.delete(group['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return group

@pytest.fixture
def agent(request, api):
    return api.agents.list().next()