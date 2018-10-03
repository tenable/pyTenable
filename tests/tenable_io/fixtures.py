import pytest, os, uuid
from tenable.tenable_io import TenableIO
from tenable.errors import *
from dateutil.parser import parse as dateparse
import datetime, sys, re

SCAN_ID_WITH_RESULTS = 1805

def check(i, name, val_type, allow_none=False):
    reuuid = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
    reuuids = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12,32}$'
    assert name in i
    if not allow_none:
        assert i[name] != None

    if i[name] != None:
        if val_type == 'datetime':
            assert isinstance(dateparse(i[name]), datetime.datetime)
        elif val_type == 'uuid':
            assert len(re.findall(reuuid, i[name])) > 0
        elif val_type == 'scanner-uuid':
            assert len(re.findall(reuuids, i[name])) > 0
        elif sys.version_info.major == 2 and val_type == str:
            assert isinstance(i[name], unicode) or isinstance(i[name], str)
        else:
            assert isinstance(i[name], val_type)

@pytest.fixture(autouse=True)
def api():
    return TenableIO(
        os.environ['TIO_TEST_ADMIN_ACCESS'], os.environ['TIO_TEST_ADMIN_SECRET'])

@pytest.fixture(autouse=True)
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

@pytest.fixture
def policy(request, api):
    policy = api.policies.create({
        'credentials': {'add': {}, 'delete': [], 'edit': {}},
        'settings': {
            'name': str(uuid.uuid4()),
        },
        'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
    })
    def teardown():
        try:
            api.policies.delete(policy['policy_id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return policy

@pytest.fixture
def user(request, api):
    user = api.users.create(
        '{}@pytenable.io'.format(uuid.uuid4()),
        '{}Tt!'.format(uuid.uuid4()),
        64)
    def teardown():
        try:
            api.users.delete(user['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return user

@pytest.fixture
def scanner(request, api):
    scanners = api.scanners.list()
    for scanner in scanners:
        if scanner['user_permissions'] == 128:
            return scanner


@pytest.fixture
def scannergroup(request, api):
    scannergroup = api.scanner_groups.create(str(uuid.uuid4()))
    def teardown():
        try:
            api.scanner_groups.delete(scannergroup['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return scannergroup

@pytest.fixture
def scan(request, api):
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'])
    def teardown():
        try:
            api.scans.delete(scan['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return scan

@pytest.fixture
def scan_results(request, api):
    return api.scans.results(SCAN_ID_WITH_RESULTS)